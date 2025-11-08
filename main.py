"""Kivy-based Ameli AI experience with integrations and chat."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

os.environ.setdefault("KIVY_CLIPBOARD", "sdl2")

from kivy.config import Config

Config.set("kivy", "clipboard", "sdl2")

from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.graphics import Color, Ellipse
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import BooleanProperty, ListProperty, NumericProperty, StringProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.uix.screenmanager import FadeTransition, Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex

from app.state import AppState, ChatMessage
from app.services.async_executor import AsyncExecutor
from app.services.config_store import ConfigStore
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

<SidebarButton@Button>:
    background_normal: ''
    background_down: ''
    size_hint_y: None
    height: dp(44)
    background_color: app.theme_surface_alt_rgba
    color: app.theme_text_primary_rgba
    bold: True

<SideBar@BoxLayout>:
    orientation: 'vertical'
    size_hint_x: None
    width: dp(96)
    padding: dp(18), dp(24)
    spacing: dp(18)
    canvas.before:
        Color:
            rgba: app.theme_surface_rgba
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(28), 0, 0, dp(28)]
    Label:
        text: 'Ameli'
        color: app.theme_text_primary_rgba
        font_size: '20sp'
        bold: True
        size_hint_y: None
        height: self.texture_size[1]
    Label:
        text: 'AI'
        color: app.theme_text_secondary_rgba
        font_size: '14sp'
        size_hint_y: None
        height: self.texture_size[1]
    Widget:
    SidebarButton:
        text: 'Home'
        on_release: app.switch_screen('home')
    SidebarButton:
        text: 'Chat'
        on_release: app.switch_screen('chat')
    SidebarButton:
        text: 'Integrations'
        on_release: app.switch_screen('integrations')
    Widget:
        size_hint_y: 1

<BackBar>:
    size_hint_y: None
    height: dp(56)
    spacing: dp(12)
    Button:
        text: '< Back'
        size_hint: None, None
        size: dp(96), dp(44)
        disabled: not root.back_enabled
        background_normal: ''
        background_down: ''
        background_color: app.theme_surface_alt_rgba
        color: app.theme_text_primary_rgba
        on_release: app.go_back()
    Label:
        text: root.title
        color: app.theme_text_primary_rgba
        font_size: '22sp'
        bold: True
        halign: 'left'
        valign: 'middle'
        size_hint_y: None
        height: self.texture_size[1]
    Widget:
        size_hint_x: 1

<IntegrationStatusItem>:
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
    height: self.ids.bubble_box.minimum_height + dp(12)
    anchor_x: 'right' if root.is_user else 'left'
    padding: dp(6), dp(6)
    BoxLayout:
        id: bubble_box
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
    canvas.before:
        Color:
            rgba: app.theme_background_rgba
        Rectangle:
            pos: self.pos
            size: self.size
    BoxLayout:
        padding: dp(24)
        spacing: dp(24)
        SideBar:
        BoxLayout:
            orientation: 'vertical'
            spacing: dp(24)
            BackBar:
                title: 'Command Center'
                back_enabled: False
            BoxLayout:
                orientation: 'horizontal'
                size_hint_y: None
                height: dp(240)
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
            AnchorLayout:
                size_hint_y: None
                height: dp(220)
                BoxLayout:
                    orientation: 'vertical'
                    size_hint: None, None
                    size: dp(220), dp(200)
                    spacing: dp(12)
                    AnchorLayout:
                        size_hint_y: None
                        height: dp(160)
                        LLMActivityIndicator:
                            size_hint: None, None
                            size: dp(160), dp(160)
                            color: app.theme_accent_rgba
                            active: app.is_llm_thinking
                    Label:
                        text: 'Awaiting reply...' if app.is_llm_thinking else 'Standing by.'
                        color: app.theme_text_secondary_rgba
                        font_size: '16sp'
                        size_hint_y: None
                        height: self.texture_size[1]
                        halign: 'center'
                        valign: 'middle'
                        text_size: self.width, None
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
    canvas.before:
        Color:
            rgba: app.theme_background_rgba
        Rectangle:
            pos: self.pos
            size: self.size
    BoxLayout:
        padding: dp(24)
        spacing: dp(24)
        SideBar:
        BoxLayout:
            orientation: 'vertical'
            spacing: dp(16)
            BackBar:
                title: 'Conversational Mode'
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
                height: dp(76)
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
    canvas.before:
        Color:
            rgba: app.theme_background_rgba
        Rectangle:
            pos: self.pos
            size: self.size
    BoxLayout:
        padding: dp(24)
        spacing: dp(24)
        SideBar:
        BoxLayout:
            orientation: 'vertical'
            spacing: dp(20)
            BackBar:
                title: 'Integration Workbench'
            ScrollView:
                do_scroll_x: False
                GridLayout:
                    id: integration_details
                    cols: 1
                    size_hint_y: None
                    height: self.minimum_height
                    spacing: dp(16)

<RootManager>:
    HomeScreen:
    ChatScreen:
    IntegrationsScreen:
"""


class IntegrationStatusItem(BoxLayout):
    """Integration status card shown on the home and integrations screens."""

    title = StringProperty("")
    status = StringProperty("")
    is_online = BooleanProperty(False)


class ChatBubble(AnchorLayout):
    """Visual representation of a chat message."""

    author = StringProperty("Ameli")
    content = StringProperty("")
    is_user = BooleanProperty(False)

    @property
    def display_author(self) -> str:
        return self.author or ("You" if self.is_user else "Ameli")


class BackBar(BoxLayout):
    """Toolbar with a back button and contextual title."""

    title = StringProperty("")
    back_enabled = BooleanProperty(True)


class LLMActivityIndicator(Widget):
    """Animated circle that pulses while the LLM is crafting a response."""

    active = BooleanProperty(False)
    pulse_scale = NumericProperty(1.0)
    orbit_offset = NumericProperty(0.0)
    color = ListProperty([0.7, 0.85, 1.0, 1.0])

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._animation: Optional[Animation] = None
        with self.canvas:
            self._halo_color = Color(rgba=(self.color[0], self.color[1], self.color[2], 0.25))
            self._halo = Ellipse()
            self._core_color = Color(rgba=self.color)
            self._core = Ellipse()
        self.bind(
            pos=self._update_canvas,
            size=self._update_canvas,
            pulse_scale=self._update_canvas,
            orbit_offset=self._update_canvas,
            color=self._update_colors,
            active=self._on_active,
        )
        self._update_canvas()
        self._update_colors()

    def _update_colors(self, *_args) -> None:
        base = self.color
        self._core_color.rgba = base
        self._halo_color.rgba = (base[0], base[1], base[2], 0.25)

    def _update_canvas(self, *_args) -> None:
        diameter = min(self.width, self.height) * 0.55 * self.pulse_scale
        halo_diameter = diameter * 1.6
        center_x = self.center_x + self.orbit_offset
        center_y = self.center_y
        self._core.size = (diameter, diameter)
        self._core.pos = (center_x - diameter / 2, center_y - diameter / 2)
        self._halo.size = (halo_diameter, halo_diameter)
        self._halo.pos = (center_x - halo_diameter / 2, center_y - halo_diameter / 2)

    def _on_active(self, *_args) -> None:
        if self.active:
            self._start_animation()
        else:
            self._stop_animation()

    def _start_animation(self) -> None:
        if self._animation:
            self._animation.stop(self)
        self._animation = (
            Animation(pulse_scale=1.2, orbit_offset=dp(18), duration=0.6, t="in_out_quad")
            + Animation(pulse_scale=0.9, orbit_offset=-dp(18), duration=0.6, t="in_out_quad")
        )
        self._animation.repeat = True
        self._animation.start(self)

    def _stop_animation(self) -> None:
        if self._animation:
            self._animation.stop(self)
            self._animation = None
        self.pulse_scale = 1.0
        self.orbit_offset = 0.0
        self._update_canvas()


class HomeScreen(Screen):
    pass


class ChatScreen(Screen):
    pass


class IntegrationsScreen(Screen):
    pass


class RootManager(ScreenManager):
    def __init__(self, **kwargs) -> None:
        kwargs.setdefault("transition", FadeTransition(duration=0.25))
        super().__init__(**kwargs)


class AmeliAIApp(App):
    """Main Kivy application for the reinvented Ameli AI experience."""

    theme_background_rgba = ListProperty([0, 0, 0, 1])
    theme_surface_rgba = ListProperty([0, 0, 0, 1])
    theme_surface_alt_rgba = ListProperty([0, 0, 0, 0.6])
    theme_accent_rgba = ListProperty([1, 1, 1, 1])
    theme_text_primary_rgba = ListProperty([1, 1, 1, 1])
    theme_text_secondary_rgba = ListProperty([0.7, 0.7, 0.7, 1])
    primary_anime_art = StringProperty("")
    is_llm_thinking = BooleanProperty(False)

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.config_store = ConfigStore(Path("ameli_settings.db"))
        self._screen_history: list[str] = []
        self.state = AppState()
        self.executor = AsyncExecutor()
        self.speech = SpeechOrchestrator()
        self.llm_router = LLMRouter()
        self.home_assistant: Optional[HomeAssistantClient] = None
        self.nextcloud: Optional[NextcloudClient] = None
        self.grocy: Optional[GrocyClient] = None
        self.vrm_registry = VRMRegistry()
        self._seed_demo_settings()
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

    def _seed_demo_settings(self) -> None:
        defaults = {
            "llm_default_model": "openrouter/mistral",
            "openrouter_api_key": "",
            "openai_api_key": "",
            "openai_model": "gpt-4o-mini",
            "elevenlabs_api_key": "",
            "elevenlabs_model": "gpt",
            "llama_local_model": "llama-1b",
            "llama_base_url": "",
            "home_assistant_url": "",
            "home_assistant_token": "",
            "nextcloud_url": "",
            "nextcloud_username": "",
            "nextcloud_password": "",
            "grocy_url": "",
            "grocy_api_key": "",
        }
        self.config_store.ensure_defaults(defaults)

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
        self.config_store.close()

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
        default_model = self.config_store.get("llm_default_model", "openrouter/mistral")
        openrouter_key = (self.config_store.get("openrouter_api_key") or "").strip()
        if openrouter_key:
            openrouter_config = LLMProviderConfig(
                provider="openrouter",
                api_key=openrouter_key,
                model=default_model,
            )
            self.llm_router.register("openrouter", openrouter_config)
            self.llm_router.register("default", openrouter_config)
        openai_key = (self.config_store.get("openai_api_key") or "").strip()
        if openai_key:
            openai_model = self.config_store.get("openai_model", "gpt-4o-mini")
            self.llm_router.register(
                "openai",
                LLMProviderConfig(provider="openai", api_key=openai_key, model=openai_model),
            )
        elevenlabs_key = (self.config_store.get("elevenlabs_api_key") or "").strip()
        if elevenlabs_key:
            elevenlabs_model = self.config_store.get("elevenlabs_model", "gpt")
            self.llm_router.register(
                "elevenlabs",
                LLMProviderConfig(provider="elevenlabs", api_key=elevenlabs_key, model=elevenlabs_model),
            )
        llama_model = self.config_store.get("llama_local_model", "llama-1b")
        llama_base_url = (self.config_store.get("llama_base_url") or "").strip() or None
        self.llm_router.register(
            "local",
            LLMProviderConfig(provider="local", model=llama_model, base_url=llama_base_url),
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
        url = (self.config_store.get("home_assistant_url") or "").strip()
        token = (self.config_store.get("home_assistant_token") or "").strip()
        if url and token:
            self.home_assistant = HomeAssistantClient(HomeAssistantConfig(base_url=url, token=token))
            status.last_error = "Connecting..."
            self.executor.submit(self.home_assistant.ping(), lambda result: self._handle_connection_result("Home Assistant", result))
        else:
            status.last_error = "Configure Home Assistant credentials in the settings database"

    def _setup_nextcloud(self) -> None:
        status = self.state.ensure_integration("Nextcloud")
        base_url = (self.config_store.get("nextcloud_url") or "").strip()
        username = (self.config_store.get("nextcloud_username") or "").strip()
        password = (self.config_store.get("nextcloud_password") or "").strip()
        if base_url and username and password:
            self.nextcloud = NextcloudClient(NextcloudConfig(base_url=base_url, username=username, password=password))
            status.is_connected = True
            status.last_error = "Ready"
        else:
            status.last_error = "Add Nextcloud details to the settings database"

    def _setup_grocy(self) -> None:
        status = self.state.ensure_integration("Grocy")
        base_url = (self.config_store.get("grocy_url") or "").strip()
        api_key = (self.config_store.get("grocy_api_key") or "").strip()
        if base_url and api_key:
            self.grocy = GrocyClient(GrocyConfig(base_url=base_url, api_key=api_key))
            status.is_connected = True
            status.last_error = "Ready"
        else:
            status.last_error = "Add Grocy connection info to the settings database"

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
        if not self.root:
            return
        current = self.root.current
        if current == name:
            return
        if name == "home":
            self._screen_history.clear()
        elif current:
            self._screen_history.append(current)
        self.root.current = name

    def go_back(self) -> None:
        if not self.root:
            return
        if self._screen_history:
            target = self._screen_history.pop()
            self.root.current = target
        else:
            self.root.current = "home"

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
        self.is_llm_thinking = True
        try:
            request = self.llm_router.ask(message)
        except Exception as exc:  # pragma: no cover - defensive pathway
            self.is_llm_thinking = False
            self._handle_llm_response(exc)
            return
        self.executor.submit(request, self._handle_llm_response)

    def _handle_llm_response(self, result: object) -> None:
        self.is_llm_thinking = False
        if isinstance(result, Exception):
            response_text = f"Error reaching LLM: {result}"
        else:
            response_text = str(result)
        reply = ChatMessage(author="Ameli", content=response_text, is_user=False)
        self.state.push_message(reply)
        self._render_chat_history()


if __name__ == "__main__":
    AmeliAIApp().run()
