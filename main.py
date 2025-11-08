"""Kivy-based Ameli AI experience with integrations and chat."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import BooleanProperty, ListProperty, StringProperty
from kivy.factory import Factory
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.uix.screenmanager import FadeTransition, Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.utils import get_color_from_hex

from app.state import AppState, ChatMessage
from app.services.async_executor import AsyncExecutor
from app.services.grocy import GrocyClient, GrocyConfig
from app.services.home_assistant import HomeAssistantClient, HomeAssistantConfig
from app.services.llm_router import LLMProviderConfig, LLMRouter
from app.services.nextcloud import NextcloudClient, NextcloudConfig
from app.services.speech import SpeechOrchestrator
from app.services.vrm import VRMAvatar, VRMRegistry
from app.ui.theme import THEME
from app.ui.utils import discover_anime_art

KV = """
#:import dp kivy.metrics.dp

<NavigationBar@BoxLayout>:
    size_hint_y: None
    height: dp(60)
    padding: dp(16)
    spacing: dp(16)
    canvas.before:
        Color:
            rgba: app.theme_surface_rgba
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(24), dp(24), dp(24), dp(24)]

<NavigationButton@Button>:
    background_normal: ''
    background_down: ''
    background_color: 0, 0, 0, 0
    color: app.theme_text_primary_rgba
    font_size: '16sp'
    bold: True

<IntegrationStatusItem@BoxLayout>:
    title: ''
    status: ''
    is_online: False
    orientation: 'vertical'
    size_hint_y: None
    height: dp(96)
    padding: dp(16)
    spacing: dp(8)
    canvas.before:
        Color:
            rgba: app.theme_surface_rgba if self.is_online else app.theme_surface_alt_rgba
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(20), dp(20), dp(20), dp(20)]
    Label:
        text: root.title
        color: app.theme_text_primary_rgba
        font_size: '18sp'
        bold: True
        size_hint_y: None
        height: self.texture_size[1]
    Label:
        text: root.status
        color: app.theme_text_secondary_rgba
        text_size: self.width, None
        halign: 'left'
        valign: 'top'
        size_hint_y: None
        height: self.texture_size[1] + dp(4)

<ChatBubble>:
    size_hint_y: None
    height: self.minimum_height + dp(12)
    anchor_x: 'right' if root.is_user else 'left'
    padding: dp(6), dp(6)
    BoxLayout:
        orientation: 'vertical'
        size_hint: None, None
        width: min(dp(540), root.width * 0.8)
        height: self.minimum_height
        padding: dp(14)
        spacing: dp(6)
        canvas.before:
            Color:
                rgba: app.chat_bubble_rgba(root.is_user)
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [dp(24), dp(24), dp(8) if root.is_user else dp(24), dp(24)]
        Label:
            text: root.display_author
            color: app.theme_text_secondary_rgba
            size_hint_y: None
            height: self.texture_size[1]
            font_size: '14sp'
            halign: 'left'
            valign: 'middle'
        Label:
            text: root.content
            color: app.theme_text_primary_rgba
            text_size: self.width, None
            size_hint_y: None
            height: self.texture_size[1]
            font_size: '16sp'
            halign: 'left'
            valign: 'top'

<HomeScreen>:
    name: 'home'
    BoxLayout:
        orientation: 'vertical'
        padding: dp(24)
        spacing: dp(24)
        canvas.before:
            Color:
                rgba: app.theme_background_rgba
            Rectangle:
                pos: self.pos
                size: self.size
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(220)
            spacing: dp(24)
            canvas.before:
                Color:
                    rgba: app.theme_surface_rgba
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [dp(32), dp(32), dp(32), dp(32)]
            AsyncImage:
                id: hero_image
                source: app.primary_anime_art
                keep_ratio: True
                allow_stretch: True
                nocache: True
                color: (1, 1, 1, 1) if app.primary_anime_art else (1, 1, 1, 0.15)
            BoxLayout:
                orientation: 'vertical'
                padding: dp(16)
                spacing: dp(12)
                Label:
                    text: 'Ameli AI Control Hub'
                    font_size: '28sp'
                    bold: True
                    color: app.theme_text_primary_rgba
                    size_hint_y: None
                    height: self.texture_size[1]
                Label:
                    text: 'Command your smart home, productivity suites and companions from one futuristic console.'
                    font_size: '16sp'
                    color: app.theme_text_secondary_rgba
                    text_size: self.width, None
                    size_hint_y: None
                    height: self.texture_size[1]
                Button:
                    text: 'Chat with Ameli'
                    size_hint: None, None
                    size: dp(200), dp(48)
                    background_normal: ''
                    background_color: app.theme_accent_rgba
                    color: app.theme_text_primary_rgba
                    on_release: app.switch_screen('chat')
        BoxLayout:
            size_hint_y: None
            height: dp(60)
            spacing: dp(16)
            NavigationButton:
                text: 'Overview'
                on_release: app.switch_screen('home')
            NavigationButton:
                text: 'Chat'
                on_release: app.switch_screen('chat')
            NavigationButton:
                text: 'Integrations'
                on_release: app.switch_screen('integrations')
        ScrollView:
            do_scroll_x: False
            bar_color: app.theme_accent_rgba
            GridLayout:
                id: status_container
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                spacing: dp(16)

<ChatScreen>:
    name: 'chat'
    BoxLayout:
        orientation: 'vertical'
        padding: dp(24)
        spacing: dp(16)
        canvas.before:
            Color:
                rgba: app.theme_background_rgba
            Rectangle:
                pos: self.pos
                size: self.size
        Label:
            text: 'Conversational Mode'
            font_size: '24sp'
            bold: True
            color: app.theme_text_primary_rgba
            size_hint_y: None
            height: self.texture_size[1]
        ScrollView:
            id: chat_scroll
            do_scroll_x: False
            bar_color: app.theme_accent_rgba
            effect_cls: 'ScrollEffect'
            GridLayout:
                id: chat_container
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                spacing: dp(12)
        BoxLayout:
            size_hint_y: None
            height: dp(64)
            spacing: dp(12)
            padding: dp(12)
            canvas.before:
                Color:
                    rgba: app.theme_surface_rgba
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [dp(20), dp(20), dp(20), dp(20)]
            TextInput:
                id: chat_input
                hint_text: 'Ask Ameli anything...'
                background_color: 0, 0, 0, 0
                foreground_color: app.theme_text_primary_rgba
                cursor_color: app.theme_text_primary_rgba
                multiline: False
                font_size: '16sp'
                write_tab: False
                on_text_validate: app.handle_chat_submission(self)
            Button:
                text: 'Send'
                size_hint_x: None
                width: dp(96)
                background_normal: ''
                background_color: app.theme_accent_rgba
                color: app.theme_text_primary_rgba
                on_release: app.handle_chat_submission(chat_input)

<IntegrationsScreen>:
    name: 'integrations'
    BoxLayout:
        orientation: 'vertical'
        padding: dp(24)
        spacing: dp(20)
        canvas.before:
            Color:
                rgba: app.theme_background_rgba
            Rectangle:
                pos: self.pos
                size: self.size
        Label:
            text: 'Integration Workbench'
            font_size: '24sp'
            bold: True
            color: app.theme_text_primary_rgba
            size_hint_y: None
            height: self.texture_size[1]
        ScrollView:
            do_scroll_x: False
            GridLayout:
                id: integration_details
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                spacing: dp(16)

<RootManager>:
    transition: FadeTransition(duration=0.25)
    HomeScreen:
    ChatScreen:
    IntegrationsScreen:
"""


class ChatBubble(AnchorLayout):
    """Visual representation of a chat message."""

    author = StringProperty("Ameli")
    content = StringProperty("")
    is_user = BooleanProperty(False)

    @property
    def display_author(self) -> str:
        return self.author or ("You" if self.is_user else "Ameli")


class HomeScreen(Screen):
    pass


class ChatScreen(Screen):
    pass


class IntegrationsScreen(Screen):
    pass


class RootManager(ScreenManager):
    pass


class AmeliAIApp(App):
    """Main Kivy application for the reinvented Ameli AI experience."""

    theme_background_rgba = ListProperty([0, 0, 0, 1])
    theme_surface_rgba = ListProperty([0, 0, 0, 1])
    theme_surface_alt_rgba = ListProperty([0, 0, 0, 0.6])
    theme_accent_rgba = ListProperty([1, 1, 1, 1])
    theme_text_primary_rgba = ListProperty([1, 1, 1, 1])
    theme_text_secondary_rgba = ListProperty([0.7, 0.7, 0.7, 1])
    primary_anime_art = StringProperty("")

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.state = AppState()
        self.executor = AsyncExecutor()
        self.speech = SpeechOrchestrator()
        self.llm_router = LLMRouter()
        self.home_assistant: Optional[HomeAssistantClient] = None
        self.nextcloud: Optional[NextcloudClient] = None
        self.grocy: Optional[GrocyClient] = None
        self.vrm_registry = VRMRegistry()
        self._setup_theme()

    def _setup_theme(self) -> None:
        self.theme_background_rgba = get_color_from_hex(THEME.background)
        self.theme_surface_rgba = get_color_from_hex(THEME.surface)
        surface_alt = list(get_color_from_hex(THEME.surface))
        if surface_alt:
            surface_alt[-1] = 0.55
        self.theme_surface_alt_rgba = surface_alt
        self.theme_accent_rgba = get_color_from_hex(THEME.accent)
        self.theme_text_primary_rgba = get_color_from_hex(THEME.text_primary)
        self.theme_text_secondary_rgba = get_color_from_hex(THEME.text_secondary)

    def build(self) -> RootManager:
        Builder.load_string(KV)
        Window.clearcolor = get_color_from_hex(THEME.background)
        Window.minimum_width, Window.minimum_height = dp(540), dp(720)
        self.title = "Ameli AI"
        icon_path = Path("ameliai_logo.png")
        if icon_path.exists():
            self.icon = str(icon_path.resolve())
        manager = RootManager()
        Clock.schedule_once(lambda _dt: self.initialize())
        return manager

    def on_stop(self) -> None:
        self.executor.shutdown()

    def initialize(self) -> None:
        self._load_anime_art()
        self._load_vrm_avatars()
        self._configure_llm_router()
        self._initialize_integrations()
        self._show_welcome_message()

    # Theme helpers -----------------------------------------------------
    def chat_bubble_rgba(self, is_user: bool) -> list[float]:
        if is_user:
            return self.theme_accent_rgba
        return self.theme_surface_rgba

    # Setup methods -----------------------------------------------------
    def _load_anime_art(self) -> None:
        search_paths = [
            Path("anim"),
            Path("media"),
            Path("assets/anime"),
        ]
        self.state.anime_art_paths = discover_anime_art(search_paths)
        if self.state.anime_art_paths:
            self.primary_anime_art = self.state.anime_art_paths[0]
        else:
            self.primary_anime_art = ""

    def _load_vrm_avatars(self) -> None:
        avatar_dir = Path("avatars")
        if avatar_dir.exists():
            for file in avatar_dir.glob("*.vrm"):
                self.vrm_registry.add_avatar(VRMAvatar(path=file, display_name=file.stem))

    def _configure_llm_router(self) -> None:
        default_model = os.getenv("AMELI_DEFAULT_MODEL", "openrouter/mistral")
        openrouter_key = os.getenv("OPENROUTER_API_KEY")
        if openrouter_key:
            self.llm_router.register(
                "openrouter",
                LLMProviderConfig(
                    provider="openrouter",
                    api_key=openrouter_key,
                    model=default_model,
                ),
            )
            self.llm_router.register("default", self.llm_router.configs["openrouter"])
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            self.llm_router.register(
                "openai",
                LLMProviderConfig(provider="openai", api_key=openai_key, model=os.getenv("OPENAI_MODEL", "gpt-4o-mini")),
            )
        elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")
        if elevenlabs_key:
            self.llm_router.register(
                "elevenlabs",
                LLMProviderConfig(provider="elevenlabs", api_key=elevenlabs_key, model=os.getenv("ELEVENLABS_MODEL", "gpt")),
            )
        llama_model = os.getenv("LLAMA_LOCAL_MODEL", "llama-1b")
        self.llm_router.register(
            "local",
            LLMProviderConfig(provider="local", model=llama_model, base_url=os.getenv("LLAMA_BASE_URL")),
        )
        if "default" not in self.llm_router.configs:
            self.llm_router.register("default", self.llm_router.configs["local"])

    def _initialize_integrations(self) -> None:
        self._setup_home_assistant()
        self._setup_nextcloud()
        self._setup_grocy()
        self._refresh_integration_cards()

    def _setup_home_assistant(self) -> None:
        status = self.state.ensure_integration("Home Assistant")
        url = os.getenv("HOME_ASSISTANT_URL")
        token = os.getenv("HOME_ASSISTANT_TOKEN")
        if url and token:
            self.home_assistant = HomeAssistantClient(HomeAssistantConfig(base_url=url, token=token))
            status.last_error = "Connecting..."
            self.executor.submit(self.home_assistant.ping(), lambda result: self._handle_connection_result("Home Assistant", result))
        else:
            status.last_error = "Set HOME_ASSISTANT_URL and HOME_ASSISTANT_TOKEN"

    def _setup_nextcloud(self) -> None:
        status = self.state.ensure_integration("Nextcloud")
        base_url = os.getenv("NEXTCLOUD_URL")
        username = os.getenv("NEXTCLOUD_USERNAME")
        password = os.getenv("NEXTCLOUD_PASSWORD")
        if base_url and username and password:
            self.nextcloud = NextcloudClient(NextcloudConfig(base_url=base_url, username=username, password=password))
            status.is_connected = True
            status.last_error = "Ready"
        else:
            status.last_error = "Configure NEXTCLOUD_URL/USERNAME/PASSWORD"

    def _setup_grocy(self) -> None:
        status = self.state.ensure_integration("Grocy")
        base_url = os.getenv("GROCY_URL")
        api_key = os.getenv("GROCY_API_KEY")
        if base_url and api_key:
            self.grocy = GrocyClient(GrocyConfig(base_url=base_url, api_key=api_key))
            status.is_connected = True
            status.last_error = "Ready"
        else:
            status.last_error = "Configure GROCY_URL and GROCY_API_KEY"

    def _handle_connection_result(self, name: str, result: object) -> None:
        status = self.state.ensure_integration(name)
        if isinstance(result, Exception):
            status.is_connected = False
            status.last_error = str(result)
        else:
            status.is_connected = bool(result)
            status.last_error = None if status.is_connected else "Connection failed"
        self._refresh_integration_cards()

    # UI rendering ------------------------------------------------------
    def _refresh_integration_cards(self) -> None:
        home_screen = self.root.get_screen("home")
        container = home_screen.ids.status_container
        container.clear_widgets()
        integration_screen = self.root.get_screen("integrations")
        integration_details = integration_screen.ids.integration_details
        integration_details.clear_widgets()
        for name, integration in self.state.integrations.items():
            card = Factory.IntegrationStatusItem(
                title=name,
                status=integration.status_label,
                is_online=integration.is_connected,
            )
            container.add_widget(card)
            description = Label(
                text=f"{name}: {integration.status_label}",
                color=self.theme_text_secondary_rgba,
                size_hint_y=None,
                height=dp(32),
                text_size=(Window.width - dp(96), None),
                halign="left",
                valign="middle",
            )
            integration_details.add_widget(description)

    def _show_welcome_message(self) -> None:
        if self.state.chat_history:
            return
        welcome = ChatMessage(author="Ameli", content="Welcome! Ask me to orchestrate your home, tasks or groceries.")
        self.state.push_message(welcome)
        self._render_chat_history()

    def switch_screen(self, name: str) -> None:
        self.root.current = name

    def _render_chat_history(self) -> None:
        chat_screen = self.root.get_screen("chat")
        container = chat_screen.ids.chat_container
        container.clear_widgets()
        for message in self.state.chat_history:
            bubble = ChatBubble(author=message.author, content=message.content, is_user=message.is_user)
            container.add_widget(bubble)

        def _scroll_to_bottom(_dt):
            chat_screen.ids.chat_scroll.scroll_y = 0

        Clock.schedule_once(_scroll_to_bottom)

    def handle_chat_submission(self, input_widget: TextInput) -> None:
        message = input_widget.text.strip()
        if not message:
            return
        input_widget.text = ""
        user_message = ChatMessage(author="You", content=message, is_user=True)
        self.state.push_message(user_message)
        self._render_chat_history()
        self.executor.submit(self.llm_router.ask(message), self._handle_llm_response)

    def _handle_llm_response(self, result: object) -> None:
        if isinstance(result, Exception):
            response_text = f"Error reaching LLM: {result}"
        else:
            response_text = str(result)
        reply = ChatMessage(author="Ameli", content=response_text, is_user=False)
        self.state.push_message(reply)
        self._render_chat_history()


if __name__ == "__main__":
    AmeliAIApp().run()
