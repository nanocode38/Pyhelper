# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive pytest tests for PyGame widgets and pghelper modules.

These tests use SDL_VIDEODRIVER=dummy (set in conftest.py) so they run
headlessly without a real display.

Covers:
  - pghelper.disassemble_sprite_sheet, load_images, draw_background
  - pghelper.Scene / SceneMgr (scene switching, request/respond, send/receive)
  - widgets.BaseConfig.set_config (and all Config classes)
  - widgets.Animate / AnimateConfig
  - widgets.CustomButton / CustomButtonConfig
  - widgets.TextButton / TextButtonConfig
  - widgets.DisplayText
  - widgets.CheckBox / CheckBoxConfig
  - widgets.Dragger
  - widgets.Image
  - widgets.RadioButtons
  - widgets.InputText / InputTextConfig
"""

import os
import time

import pygame
import pytest

from pyhelper.gamehelpers.pghelper import (
    Scene,
    SceneMgr,
    disassemble_sprite_sheet,
    draw_background,
    load_images,
)
from pyhelper.gamehelpers.pghelper.widgets import (
    Animate,
    AnimateConfig,
    BaseConfig,
    CheckBox,
    CheckBoxConfig,
    CustomButton,
    CustomButtonConfig,
    DisplayText,
    Dragger,
    Image,
    InputText,
    InputTextConfig,
    RadioButtons,
    TextButton,
    TextButtonConfig,
)

# ---------------------------------------------------------------------------
#  Path helpers
# ---------------------------------------------------------------------------
_IMAGES_DIR = os.path.join("gamehelpers", "images")


def _img(name: str) -> str:
    """Return the full relative path to a test image."""
    return os.path.join(_IMAGES_DIR, name)


# ---------------------------------------------------------------------------
#  Fixtures
# ---------------------------------------------------------------------------
@pytest.fixture
def screen():
    """Create a small off-screen Surface for widget tests."""
    pygame.init()
    surf = pygame.display.set_mode((800, 600))
    yield surf
    pygame.display.quit()


@pytest.fixture
def surface():
    """Create a plain Surface (no display needed)."""
    pygame.init()
    return pygame.Surface((800, 600))


# ===========================================================================
#  pghelper.__init__ — disassemble_sprite_sheet / load_images / draw_background
# ===========================================================================
class TestDisassembleSpriteSheet:
    """Tests for disassemble_sprite_sheet()."""

    def test_returns_list_of_surfaces(self, screen):
        images = disassemble_sprite_sheet(_img("f1.gif"), 50, 50, 1)
        assert isinstance(images, list)
        assert len(images) == 1
        assert isinstance(images[0], pygame.Surface)

    def test_multiple_images(self, screen):
        # f1..f10 are individual frames, so we only test with 1 per sheet
        images = disassemble_sprite_sheet(_img("f1.gif"), 25, 25, 1)
        assert len(images) == 1

    def test_zero_images(self, screen):
        images = disassemble_sprite_sheet(_img("f1.gif"), 50, 50, 0)
        assert images == []


class TestLoadImages:
    """Tests for load_images()."""

    def test_load_multiple(self):
        paths = [_img(f"f{i}.gif") for i in range(1, 6)]
        images = load_images(paths)
        assert len(images) == 5
        assert all(isinstance(img, pygame.Surface) for img in images)

    def test_load_single(self):
        images = load_images([_img("pythonIcon.png")])
        assert len(images) == 1

    def test_returns_list_not_iterator(self):
        images = load_images(iter([_img("f1.gif")]))
        assert isinstance(images, list)
        # Should be usable multiple times
        assert len(images) == 1
        assert len(images) == 1


class TestDrawBackground:
    """Tests for draw_background / Background."""

    def test_blits_to_screen(self, screen):
        draw_background(screen, _img("background.jpg"))
        # After blitting, the screen should not be entirely black
        assert screen.get_at((0, 0)) != (0, 0, 0, 255)

    def test_scaled_width(self, screen):
        draw_background(screen, _img("background.jpg"), width=400)
        assert screen.get_at((0, 0)) != (0, 0, 0, 255)

    def test_scaled_height(self, screen):
        draw_background(screen, _img("background.jpg"), height=300)
        assert screen.get_at((0, 0)) != (0, 0, 0, 255)

    def test_fullscreen_width(self, screen):
        draw_background(screen, _img("background.jpg"), width=pygame.FULLSCREEN)
        assert screen.get_at((0, 0)) != (0, 0, 0, 255)

    def test_cached_on_second_call(self, screen):
        """Background caches the image after first call."""
        draw_background(screen, _img("background.jpg"))
        # Second call should use cached image (same path, same screen size)
        draw_background(screen, _img("background.jpg"))
        assert screen.get_at((0, 0)) != (0, 0, 0, 255)


# ===========================================================================
#  BaseConfig
# ===========================================================================
class TestBaseConfig:
    """Tests for BaseConfig.set_config()."""

    def test_set_config_valid_attr(self, screen):
        cfg = TextButtonConfig(screen)
        cfg.set_config("text", "New Text")
        assert cfg.text == "New Text"

    def test_set_config_invalid_attr_raises(self, screen):
        cfg = TextButtonConfig(screen)
        with pytest.raises(ValueError, match="did not have attribute"):
            cfg.set_config("nonexistent_attr", 123)

    def test_set_config_width(self, screen):
        cfg = TextButtonConfig(screen)
        cfg.set_config("width", 300)
        assert cfg.width == 300


# ===========================================================================
#  AnimateConfig / Animate
# ===========================================================================
class TestAnimateConfig:
    """Tests for AnimateConfig."""

    def test_defaults(self, screen):
        paths = [_img(f"f{i}.gif") for i in range(1, 4)]
        cfg = AnimateConfig(screen, paths)
        assert cfg.autostart is False
        assert cfg.show_first_image_at_end is True
        assert cfg.loop is False
        assert cfg.nloop == 1
        assert cfg.duration == 0.1
        assert len(cfg.images) == 3

    def test_with_surface_objects(self, screen):
        paths = [_img(f"f{i}.gif") for i in range(1, 4)]
        surfaces = load_images(paths)
        cfg = AnimateConfig(screen, surfaces)
        assert len(cfg.images) == 3
        assert all(isinstance(img, pygame.Surface) for img in cfg.images)


class TestAnimate:
    """Tests for Animate."""

    @pytest.fixture
    def animate(self, screen):
        paths = [_img(f"f{i}.gif") for i in range(1, 4)]
        cfg = AnimateConfig(screen, paths)
        return Animate(cfg)

    def test_init_without_autostart(self, animate):
        assert animate.playing is False
        assert animate.nimage == 3

    def test_play(self, animate):
        animate.play()
        assert animate.playing is True

    def test_pause(self, animate):
        animate.play()
        animate.pause()
        assert animate._pause is True

    def test_update_when_not_playing(self, animate):
        """update() should do nothing when not playing."""
        animate.update()  # should not raise
        assert animate.index == 0

    def test_draw(self, animate):
        animate.play()
        animate.draw()  # should not raise

    def test_autostart(self, screen):
        paths = [_img(f"f{i}.gif") for i in range(1, 4)]
        cfg = AnimateConfig(screen, paths)
        cfg.autostart = True
        anim = Animate(cfg)
        assert anim.playing is True

    def test_loop_behavior(self, screen):
        paths = [_img(f"f{i}.gif") for i in range(1, 4)]
        cfg = AnimateConfig(screen, paths)
        cfg.loop = True
        cfg.duration = 0  # switch images immediately
        anim = Animate(cfg)
        anim.play()
        # Simulate frame updates
        time.sleep(0.01)
        anim.update()
        # With loop=True, the animation should still be playing after all frames
        # (We can't easily test full loop without sleeping, but we verify it's playing)
        assert anim.playing is True


# ===========================================================================
#  CustomButtonConfig / CustomButton
# ===========================================================================
class TestCustomButtonConfig:
    """Tests for CustomButtonConfig."""

    def test_defaults(self, screen):
        cfg = CustomButtonConfig(screen, [_img("ButtonUp.png")])
        assert cfg.text == ""
        assert cfg.font_size == 20
        assert cfg.command is None
        assert cfg.args == ()
        assert cfg.sounds_on_chick is None

    def test_with_multiple_images(self, screen):
        cfg = CustomButtonConfig(
            screen,
            [
                _img("ButtonUp.png"),
                _img("ButtonDown.png"),
                _img("ButtonOver.png"),
                _img("ButtonLock.png"),
            ],
        )
        assert len(cfg.images) == 4


class TestCustomButton:
    """Tests for CustomButton."""

    @pytest.fixture
    def button(self, screen):
        cfg = CustomButtonConfig(
            screen,
            [
                _img("ButtonUp.png"),
                _img("ButtonDown.png"),
                _img("ButtonOver.png"),
                _img("ButtonLock.png"),
            ],
        )
        cfg.text = "Click Me"
        return CustomButton(cfg)

    def test_init(self, button):
        assert button.text == "Click Me"
        assert button.hidden is False
        assert button.lock is False

    def test_is_chick_not_mouseup(self, button):
        event = pygame.event.Event(pygame.MOUSEMOTION)
        assert button.is_chick(event) is False

    def test_is_chick_hidden(self, button):
        button.hidden = True
        event = pygame.event.Event(pygame.MOUSEBUTTONUP, {"pos": (0, 0), "button": 1})
        assert button.is_chick(event) is False

    def test_is_chick_locked(self, button):
        button.lock = True
        event = pygame.event.Event(pygame.MOUSEBUTTONUP, {"pos": (0, 0), "button": 1})
        assert button.is_chick(event) is False

    def test_is_hover_returns_bool(self, button):
        result = button.is_hover()
        assert isinstance(result, bool)

    def test_is_hover_hidden(self, button):
        button.hidden = True
        assert button.is_hover() is False

    def test_update_with_mousemotion(self, button):
        event = pygame.event.Event(pygame.MOUSEMOTION, {"pos": (0, 0)})
        button.update(event)  # should not raise

    def test_draw(self, button):
        button.draw()  # should not raise

    def test_draw_hidden(self, button):
        button.hidden = True
        button.draw()  # should be a no-op

    def test_lock_state(self, button):
        button.lock = True
        event = pygame.event.Event(pygame.MOUSEMOTION, {"pos": (0, 0)})
        button.update(event)
        # When locked, image should be lock_image
        assert button.image == button.lock_image

    def test_command_called_on_click(self, screen):
        results = []
        cfg = CustomButtonConfig(screen, [_img("ButtonUp.png"), _img("ButtonDown.png")])
        cfg.command = lambda: results.append("clicked")
        cfg.args = ()
        btn = CustomButton(cfg)
        # Simulate MOUSEBUTTONDOWN then MOUSEBUTTONUP on the button
        pos = btn.rect.center
        down_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": pos, "button": 1})
        btn.update(down_event)
        up_event = pygame.event.Event(pygame.MOUSEBUTTONUP, {"pos": pos, "button": 1})
        btn.update(up_event)
        assert results == ["clicked"]


# ===========================================================================
#  TextButtonConfig / TextButton
# ===========================================================================
class TestTextButtonConfig:
    """Tests for TextButtonConfig."""

    def test_defaults(self, screen):
        cfg = TextButtonConfig(screen)
        assert cfg.width == 180
        assert cfg.height == 50
        assert cfg.text == "Hello World!"
        assert cfg.command is None
        assert cfg.args == ()

    def test_set_config(self, screen):
        cfg = TextButtonConfig(screen)
        cfg.set_config("text", "Custom")
        assert cfg.text == "Custom"


class TestTextButton:
    """Tests for TextButton."""

    @pytest.fixture
    def button(self, screen):
        cfg = TextButtonConfig(screen)
        cfg.text = "Test Button"
        return TextButton(cfg)

    def test_constants(self):
        assert TextButton.BUTTON_UP == 0
        assert TextButton.BUTTON_DOWN == 1
        assert TextButton.BUTTON_OVER == 2
        assert TextButton.BUTTON_LOCK == 3

    def test_init(self, button):
        assert button.text == "Test Button"
        assert button.mode == TextButton.BUTTON_UP
        assert button.lock is False
        assert button.hidden is False

    def test_is_chick_down(self, button):
        pos = button.rect.center
        pygame.mouse.set_pos(pos)
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": pos, "button": 1})
        assert button.is_chick_down(event) is True

    def test_is_chick_down_outside(self, button):
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (-100, -100), "button": 1})
        assert button.is_chick_down(event) is False

    def test_button_is_chick(self, button):
        pos = button.rect.center
        pygame.mouse.set_pos(pos)
        event = pygame.event.Event(pygame.MOUSEBUTTONUP, {"pos": pos, "button": 1})
        assert button.button_is_chick(event) is True

    def test_button_is_chick_wrong_type(self, button):
        event = pygame.event.Event(pygame.MOUSEMOTION, {"pos": button.rect.center})
        assert button.button_is_chick(event) is False

    def test_button_is_hover(self, button):
        pos = button.rect.center
        pygame.mouse.set_pos(pos)
        event = pygame.event.Event(pygame.MOUSEMOTION, {"pos": pos})
        assert button.button_is_hover(event) is True

    def test_button_is_hover_on_click(self, button):
        pos = button.rect.center
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": pos, "button": 1})
        assert button.button_is_hover(event) is False

    def test_update_hidden(self, button):
        button.hidden = True
        event = pygame.event.Event(pygame.MOUSEMOTION, {"pos": (0, 0)})
        assert button.update(event) is False

    def test_update_locked(self, button):
        button.lock = True
        event = pygame.event.Event(pygame.MOUSEMOTION, {"pos": (0, 0)})
        assert button.update(event) is False
        assert button.mode == TextButton.BUTTON_LOCK

    def test_draw_all_modes(self, button):
        for mode in (TextButton.BUTTON_UP, TextButton.BUTTON_DOWN,
                     TextButton.BUTTON_OVER, TextButton.BUTTON_LOCK):
            button.mode = mode
            button.draw()  # should not raise

    def test_command_on_click(self, screen):
        results = []
        cfg = TextButtonConfig(screen)
        cfg.command = lambda: results.append("clicked")
        btn = TextButton(cfg)
        pos = btn.rect.center
        pygame.mouse.set_pos(pos)
        # Simulate click: down then up
        btn.update(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": pos, "button": 1}))
        result = btn.update(pygame.event.Event(pygame.MOUSEBUTTONUP, {"pos": pos, "button": 1}))
        assert result is True
        assert results == ["clicked"]


# ===========================================================================
#  DisplayText
# ===========================================================================
class TestDisplayText:
    """Tests for DisplayText."""

    def test_init(self, screen):
        dt = DisplayText(screen, text="Hello", size=24)
        assert dt.text == "Hello"

    def test_set_value_text_only(self, screen):
        dt = DisplayText(screen, text="Old")
        dt.set_value("New")
        assert dt.text == "New"

    def test_set_value_color_only(self, screen):
        dt = DisplayText(screen, text="Hello")
        dt.set_value(new_color=(255, 0, 0))
        assert dt.color == (255, 0, 0)

    def test_set_value_both(self, screen):
        dt = DisplayText(screen, text="Old")
        dt.set_value("New", (0, 255, 0))
        assert dt.text == "New"
        assert dt.color == (0, 255, 0)

    def test_draw(self, screen):
        dt = DisplayText(screen, text="Test")
        dt.draw()  # should not raise

    def test_default_color(self, screen):
        dt = DisplayText(screen)
        assert dt.color == (255, 255, 255)


# ===========================================================================
#  CheckBoxConfig / CheckBox
# ===========================================================================
class TestCheckBoxConfig:
    """Tests for CheckBoxConfig."""

    def test_defaults(self, screen):
        cfg = CheckBoxConfig(screen)
        assert cfg.text == "CheckBox"
        assert cfg.font is None
        assert cfg.text_color == (255, 255, 255)
        assert cfg.image_paths == ("CheckBox",)


class TestCheckBox:
    """Tests for CheckBox."""

    @pytest.fixture
    def checkbox(self, screen):
        cfg = CheckBoxConfig(screen)
        cfg.text = "Test Box"
        cfg.image_paths = (
            _img("checkBoxOnUp.png"),
            _img("checkBoxOnDown.png"),
            _img("checkBoxOffUp.png"),
            _img("checkBoxOffDown.png"),
        )
        return CheckBox(cfg)

    def test_init(self, checkbox):
        assert checkbox.text == "Test Box"
        assert checkbox.is_check is False
        assert checkbox.lock is False

    def test_update_no_event(self, checkbox):
        event = pygame.event.Event(pygame.MOUSEMOTION, {"pos": (0, 0)})
        result = checkbox.update(event)
        assert result is False

    def test_update_click_inside(self, checkbox):
        pos = checkbox.rect.center
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": pos, "button": 1})
        result = checkbox.update(event)
        assert result is True
        assert checkbox.is_check is True

    def test_update_click_outside(self, checkbox):
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (-100, -100), "button": 1})
        result = checkbox.update(event)
        assert result is False
        assert checkbox.is_check is False

    def test_toggle(self, checkbox):
        pos = checkbox.rect.center
        # First click: check
        checkbox.update(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": pos, "button": 1}))
        assert checkbox.is_check is True
        # Second click: uncheck
        checkbox.update(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": pos, "button": 1}))
        assert checkbox.is_check is False

    def test_draw(self, checkbox):
        checkbox.draw()  # should not raise

    def test_locked_no_toggle(self, checkbox):
        checkbox.lock = True
        pos = checkbox.rect.center
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": pos, "button": 1})
        result = checkbox.update(event)
        assert result is False  # locked checkboxes don't toggle


# ===========================================================================
#  Dragger
# ===========================================================================
class TestDragger:
    """Tests for Dragger."""

    @pytest.fixture
    def dragger(self, screen):
        return Dragger(
            screen,
            (
                _img("dragMeUp.png"),
                _img("dragMeDown.png"),
                _img("dragMeOver.png"),
                _img("dragMeDisabled.png"),
            ),
        )

    def test_init(self, dragger):
        assert dragger.hidden is False
        assert dragger.lock is False
        assert isinstance(dragger.image, pygame.Surface)

    def test_is_drag_not_mousedown(self, dragger):
        event = pygame.event.Event(pygame.MOUSEMOTION, {"pos": (0, 0)})
        assert dragger.is_drag(event) is False

    def test_is_drag_hidden(self, dragger):
        dragger.hidden = True
        pos = dragger.rect.center
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": pos, "button": 1})
        assert dragger.is_drag(event) is False

    def test_is_drag_locked(self, dragger):
        dragger.lock = True
        pos = dragger.rect.center
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": pos, "button": 1})
        assert dragger.is_drag(event) is False

    def test_is_hover(self, dragger):
        pos = dragger.rect.center
        event = pygame.event.Event(pygame.MOUSEMOTION, {"pos": pos})
        assert dragger.is_hover(event) is True

    def test_is_hover_hidden(self, dragger):
        dragger.hidden = True
        event = pygame.event.Event(pygame.MOUSEMOTION, {"pos": (0, 0)})
        assert dragger.is_hover(event) is False

    def test_update_mousemotion(self, dragger):
        event = pygame.event.Event(pygame.MOUSEMOTION, {"pos": (0, 0)})
        dragger.update(event)  # should not raise

    def test_draw(self, dragger):
        dragger.draw()  # should not raise

    def test_draw_hidden(self, dragger):
        dragger.hidden = True
        dragger.draw()  # should be a no-op

    def test_single_image_fallback(self, screen):
        """When only one image is provided, all states use it."""
        # Pass Surface objects directly so all states share the same object
        surf = pygame.Surface((50, 50))
        d = Dragger(screen, (surf,))
        assert d.up_image is d.down_image
        assert d.up_image is d.over_image
        assert d.up_image is d.lock_image


# ===========================================================================
#  Image
# ===========================================================================
class TestImage:
    """Tests for Image widget."""

    @pytest.fixture
    def image(self, screen):
        return Image(screen, _img("pythonIcon.png"), loc=(10, 10))

    def test_init_with_loc(self, screen):
        img = Image(screen, _img("pythonIcon.png"), loc=(50, 50))
        assert img.rect.topleft == (50, 50)

    def test_init_with_rect(self, screen):
        rect = pygame.Rect(100, 200, 50, 50)
        img = Image(screen, _img("pythonIcon.png"), rect=rect)
        assert img.rect == rect

    def test_init_no_loc_no_rect_raises(self, screen):
        with pytest.raises(ValueError, match="loc or rect must be specified"):
            Image(screen, _img("pythonIcon.png"))

    def test_flip_horizontal(self, image):
        original = image.image
        image.flip(flip_horizontal=True)
        assert image.image is not original

    def test_flip_vertical(self, image):
        image.flip(flip_vertical=True)

    def test_set_move(self, image):
        original_x = image.rect.centerx
        image.set_move(x=10, y=5)
        assert image.rect.centerx == original_x + 10

    def test_rot_center(self, image):
        image.rot_center(45)

    def test_set_position(self, image):
        image.set_position(100, 200)
        assert image.rect.center == (100, 200)

    def test_scale(self, image):
        image.scale(100, 100)
        assert image.image.get_width() == 100
        assert image.image.get_height() == 100

    def test_get_rect(self, image):
        assert isinstance(image.get_rect(), pygame.Rect)

    def test_draw(self, image):
        image.draw()  # should not raise

    def test_draw_hidden(self, image):
        image.hidden = True
        image.draw()  # should be a no-op

    def test_hidden_flag(self, image):
        assert image.hidden is False
        image.hidden = True
        assert image.hidden is True


# ===========================================================================
#  RadioButtons
# ===========================================================================
class TestRadioButtons:
    """Tests for RadioButtons."""

    @pytest.fixture
    def radio_buttons(self, screen):
        buttons = []
        for i in range(3):
            cfg = CheckBoxConfig(screen)
            cfg.text = f"Option {i+1}"
            cfg.image_paths = (
                _img("checkBoxOnUp.png"),
                _img("checkBoxOnDown.png"),
                _img("checkBoxOffUp.png"),
                _img("checkBoxOffDown.png"),
            )
            cb = CheckBox(cfg)
            buttons.append(cb)
        return RadioButtons(screen, buttons)

    def test_init(self, radio_buttons):
        assert len(radio_buttons.buttons) == 3
        assert radio_buttons._last_button is None

    def test_update_no_event(self, radio_buttons):
        event = pygame.event.Event(pygame.MOUSEMOTION, {"pos": (0, 0)})
        radio_buttons.update(event)  # should not raise

    def test_update_click_first_button(self, radio_buttons):
        pos = radio_buttons.buttons[0].rect.center
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": pos, "button": 1})
        radio_buttons.update(event)
        assert radio_buttons.buttons[0].is_check is True
        assert radio_buttons._last_button is radio_buttons.buttons[0]

    def test_update_switch_selection(self, radio_buttons):
        # Click first button
        pos0 = radio_buttons.buttons[0].rect.center
        radio_buttons.update(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": pos0, "button": 1}))
        assert radio_buttons.buttons[0].is_check is True
        # Click second button
        pos1 = radio_buttons.buttons[1].rect.center
        radio_buttons.update(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": pos1, "button": 1}))
        assert radio_buttons.buttons[1].is_check is True
        assert radio_buttons.buttons[0].is_check is False

    def test_get_focus_none(self, radio_buttons):
        assert radio_buttons.get_focus() is None

    def test_get_focus_selected(self, radio_buttons):
        pos = radio_buttons.buttons[0].rect.center
        radio_buttons.update(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": pos, "button": 1}))
        assert radio_buttons.get_focus() == 0

    def test_draw(self, radio_buttons):
        radio_buttons.draw()  # should not raise


# ===========================================================================
#  InputTextConfig / InputText
# ===========================================================================
class TestInputTextConfig:
    """Tests for InputTextConfig."""

    def test_defaults(self, screen):
        cfg = InputTextConfig(screen)
        assert cfg.loc == (0, 0)
        assert cfg.color == (255, 255, 255)
        assert cfg.text_color == (0, 0, 0)
        assert cfg.value == ""
        assert cfg.width == 250
        assert cfg.font_size == 30
        assert cfg.command is None
        assert cfg.focus_color == (0, 0, 0)
        assert cfg.init_focus is False
        assert cfg.mask is None
        assert cfg.keep_focus_on_submit is False

    def test_set_config(self, screen):
        cfg = InputTextConfig(screen)
        cfg.set_config("value", "Hello")
        assert cfg.value == "Hello"


class TestInputText:
    """Tests for InputText."""

    @pytest.fixture
    def input_text(self, screen):
        cfg = InputTextConfig(screen)
        cfg.value = "Initial"
        cfg.loc = (100, 100)
        return InputText(cfg)

    def test_get_value(self, input_text):
        assert input_text.get_value() == "Initial"

    def test_set_value(self, input_text):
        input_text.set_value("New Text")
        assert input_text.get_value() == "New Text"

    def test_is_focus_default_false(self, input_text):
        assert input_text.is_focus() is False

    def test_give_focus(self, input_text):
        input_text.give_focus()
        assert input_text.is_focus() is True

    def test_remove_focus(self, input_text):
        input_text.give_focus()
        input_text.remove_focus()
        assert input_text.is_focus() is False

    def test_clear(self, input_text):
        input_text.clear()
        assert input_text.get_value() == ""

    def test_clear_keep_focus(self, input_text):
        input_text.give_focus()
        input_text.clear(keep_focus=True)
        assert input_text.get_value() == ""
        assert input_text.is_focus() is True

    def test_set_loc(self, input_text):
        input_text.set_loc((200, 300))
        assert input_text.loc == (200, 300)

    def test_set_next_field_on_tab(self, input_text):
        input_text.set_next_field_on_tab("next_field")
        # This is stored as a private attribute, just verify it doesn't raise

    def test_draw(self, input_text):
        input_text.draw()  # should not raise

    def test_draw_hidden(self, input_text):
        input_text.hidden = True
        input_text.draw()  # should be a no-op

    def test_update_disabled(self, input_text):
        input_text.is_enabled = False
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (0, 0), "button": 1})
        assert input_text.update(event) is False

    def test_update_hidden(self, input_text):
        input_text.hidden = True
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (0, 0), "button": 1})
        assert input_text.update(event) is False

    def test_click_inside_gives_focus(self, input_text):
        pos = input_text.loc
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": pos, "button": 1})
        result = input_text.update(event)
        assert input_text.is_focus() is True
        assert result is False

    def test_click_outside_removes_focus(self, input_text):
        input_text.give_focus()
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (-100, -100), "button": 1})
        input_text.update(event)
        assert input_text.is_focus() is False

    def test_backspace_key(self, input_text):
        input_text.give_focus()
        event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_BACKSPACE})
        input_text.update(event)
        assert input_text.get_value() == "Initia"

    def test_delete_key(self, input_text):
        input_text.give_focus()
        # Move cursor to start
        event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_HOME})
        input_text.update(event)
        # Delete forward
        event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_DELETE})
        input_text.update(event)
        assert input_text.get_value() == "nitial"

    def test_right_arrow(self, input_text):
        input_text.give_focus()
        # Cursor should be at end; moving right does nothing
        original_pos = input_text.cursor_position
        event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RIGHT})
        input_text.update(event)
        assert input_text.cursor_position == original_pos

    def test_left_arrow(self, input_text):
        input_text.give_focus()
        original_pos = input_text.cursor_position
        event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_LEFT})
        input_text.update(event)
        assert input_text.cursor_position == original_pos - 1

    def test_home_key(self, input_text):
        input_text.give_focus()
        event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_HOME})
        input_text.update(event)
        assert input_text.cursor_position == 0

    def test_end_key(self, input_text):
        input_text.give_focus()
        # Move to home first
        input_text.update(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_HOME}))
        # Then to end
        input_text.update(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_END}))
        assert input_text.cursor_position == len(input_text.get_value())

    def test_typing_text(self, input_text):
        input_text.give_focus()
        event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_a, "unicode": "a"})
        input_text.update(event)
        assert input_text.get_value() == "Initiala"

    def test_enter_key_returns_true(self, input_text):
        input_text.give_focus()
        event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN, "unicode": ""})
        result = input_text.update(event)
        assert result is True

    def test_enter_key_calls_command(self, screen):
        results = []
        cfg = InputTextConfig(screen)
        cfg.command = lambda: results.append("submitted")
        cfg.args = ()
        it = InputText(cfg)
        it.give_focus()
        event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN, "unicode": ""})
        it.update(event)
        assert results == ["submitted"]

    def test_mask_mode(self, screen):
        cfg = InputTextConfig(screen)
        cfg.value = "secret"
        cfg.mask = "*"
        it = InputText(cfg)
        assert it.mask == "*"
        assert it.get_value() == "secret"

    def test_init_focus(self, screen):
        cfg = InputTextConfig(screen)
        cfg.init_focus = True
        it = InputText(cfg)
        assert it.is_focus() is True

    def test_keep_focus_on_submit(self, screen):
        cfg = InputTextConfig(screen)
        cfg.init_focus = True
        cfg.keep_focus_on_submit = True
        it = InputText(cfg)
        event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN, "unicode": ""})
        it.update(event)
        assert it.is_focus() is True


# ===========================================================================
#  Scene / SceneMgr
# ===========================================================================
class TestScene:
    """Tests for Scene abstract class and SceneMgr."""

    @pytest.fixture
    def scenes(self, screen):
        """Create three concrete Scene subclasses for testing."""

        class SceneA(Scene):
            def __init__(self, screen):
                self.screen = screen
                self.screen_rect = screen.get_rect()
                self.entered = False
                self.left = False
                self.respond_data = "data_from_A"
                self.received = []

            def get_scene_key(self):
                return "A"

            def update(self, events, key_pressed_list):
                pass

            def draw(self):
                self.screen.fill((255, 0, 0))

            def enter(self, data=None):
                self.entered = True
                self.enter_data = data

            def leave(self):
                self.left = True

            def respond(self, request_id):
                return self.respond_data

            def receive(self, receive_id, info):
                self.received.append((receive_id, info))

        class SceneB(Scene):
            def __init__(self, screen):
                self.screen = screen
                self.screen_rect = screen.get_rect()
                self.received = []

            def get_scene_key(self):
                return "B"

            def update(self, events, key_pressed_list):
                pass

            def draw(self):
                self.screen.fill((0, 255, 0))

            def receive(self, receive_id, info):
                self.received.append((receive_id, info))

        class SceneC(Scene):
            def __init__(self, screen):
                self.screen = screen
                self.screen_rect = screen.get_rect()
                self.received = []

            def get_scene_key(self):
                return "C"

            def update(self, events, key_pressed_list):
                pass

            def draw(self):
                self.screen.fill((0, 0, 255))

            def receive(self, receive_id, info):
                self.received.append((receive_id, info))

        return {"A": SceneA(screen), "B": SceneB(screen), "C": SceneC(screen)}, SceneA

    def test_scene_mgr_init_with_dict(self, scenes, screen):
        scene_dict, _ = scenes
        mgr = SceneMgr(scene_dict, 30)
        assert mgr.fps == 30
        assert mgr.current_scene is scene_dict["A"]
        assert mgr.show_frame_rate is False

    def test_scene_mgr_init_with_list(self, screen):
        class TestScene1(Scene):
            def __init__(self, screen):
                self.screen = screen
                self.screen_rect = screen.get_rect()

            def get_scene_key(self):
                return "test1"

            def update(self, events, key_pressed_list):
                pass

            def draw(self):
                pass

        class TestScene2(Scene):
            def __init__(self, screen):
                self.screen = screen
                self.screen_rect = screen.get_rect()

            def get_scene_key(self):
                return "test2"

            def update(self, events, key_pressed_list):
                pass

            def draw(self):
                pass

        scene_list = [TestScene1(screen), TestScene2(screen)]
        mgr = SceneMgr(scene_list, 60)
        assert mgr.current_scene is scene_list[0]
        assert "test1" in mgr.scenes_dict
        assert "test2" in mgr.scenes_dict

    def test_scene_mgr_frame_rate_display(self, scenes, screen):
        scene_dict, _ = scenes
        fps_display = DisplayText(screen, text="FPS: 0")
        mgr = SceneMgr(scene_dict, 30, frame_rate_display=fps_display)
        assert mgr.show_frame_rate is True

    def test_go_to_scene(self, scenes, screen):
        scene_dict, SceneA = scenes
        mgr = SceneMgr(scene_dict, 30)
        scene_a = scene_dict["A"]
        # Verify initial scene is A
        assert mgr.current_scene is scene_a
        # Go to scene B
        scene_a.go_to_scene("B")
        assert mgr.current_scene is scene_dict["B"]
        # Scene A should have been left
        assert scene_a.left is True
        # Scene B should have been entered
        assert mgr.current_scene is scene_dict["B"]

    def test_go_to_scene_with_data(self, scenes, screen):
        scene_dict, SceneA = scenes
        mgr = SceneMgr(scene_dict, 30)
        scene_a = scene_dict["A"]
        scene_a.go_to_scene("B", data="custom_data")
        # Scene B's enter() is the default (pass), so no error

    def test_go_to_invalid_scene_raises(self, scenes, screen):
        scene_dict, _ = scenes
        mgr = SceneMgr(scene_dict, 30)
        with pytest.raises(KeyError):
            mgr.current_scene.go_to_scene("nonexistent")

    def test_quit_scene(self, scenes, screen):
        scene_dict, _ = scenes
        mgr = SceneMgr(scene_dict, 30)
        with pytest.raises(SystemExit):
            mgr.current_scene.quit()

    def test_request_respond(self, scenes, screen):
        scene_dict, SceneA = scenes
        mgr = SceneMgr(scene_dict, 30)
        scene_a = scene_dict["A"]
        # A requests from itself (A implements respond, returns "data_from_A")
        result = scene_a.request("A", "some_request")
        assert result == "data_from_A"

    def test_send_receive(self, scenes, screen):
        scene_dict, SceneA = scenes
        mgr = SceneMgr(scene_dict, 30)
        scene_a = scene_dict["A"]
        scene_b = scene_dict["B"]
        # Scene B sends data to Scene A
        scene_b.send("A", "test_id", "test_info")
        assert scene_a.received[-1] == ("test_id", "test_info")

    def test_send_all(self, scenes, screen):
        scene_dict, SceneA = scenes
        mgr = SceneMgr(scene_dict, 30)
        scene_a = scene_dict["A"]
        scene_b = scene_dict["B"]
        scene_c = scene_dict["C"]
        scene_a.send_all("broadcast", "hello")
        # B and C should have received it
        assert ("broadcast", "hello") in scene_b.received
        assert ("broadcast", "hello") in scene_c.received
        # A should NOT have received it (sender excluded)
        assert all(r[0] != "broadcast" for r in scene_a.received)

    def test_respond_not_implemented(self, scenes, screen):
        scene_dict, _ = scenes
        mgr = SceneMgr(scene_dict, 30)
        scene_b = scene_dict["B"]
        # Scene B doesn't implement respond()
        with pytest.raises(NotImplementedError):
            scene_b.respond("request")

    def test_receive_not_implemented(self, scenes, screen):
        """Base Scene.receive() raises NotImplementedError."""
        scene_dict, _ = scenes
        mgr = SceneMgr(scene_dict, 30)

        class BareScene(Scene):
            def __init__(self, screen):
                self.screen = screen
                self.screen_rect = screen.get_rect()

            def get_scene_key(self):
                return "bare"

            def update(self, events, key_pressed_list):
                pass

            def draw(self):
                pass

        bare = BareScene(screen)
        with pytest.raises(NotImplementedError):
            bare.receive("id", "info")

    @pytest.mark.xfail(reason="Source bug: _add_scene() signature mismatch + calls nonexistent getSceneKey()")
    def test_add_scene(self, scenes, screen):
        scene_dict, _ = scenes
        mgr = SceneMgr(scene_dict, 30)

        class SceneD(Scene):
            def __init__(self, screen):
                self.screen = screen
                self.screen_rect = screen.get_rect()

            def get_scene_key(self):
                return "D"

            def update(self, events, key_pressed_list):
                pass

            def draw(self):
                pass

        new_scene = SceneD(screen)
        mgr.current_scene.add_scene("D", new_scene)
        assert "D" in mgr.scenes_dict

    def test_remove_scene(self, scenes, screen):
        scene_dict, _ = scenes
        mgr = SceneMgr(scene_dict, 30)
        mgr.current_scene.remove_scene("C")
        assert "C" in mgr.scenes_to_remove_list

    def test_remove_nonexistent_scene_raises(self, scenes, screen):
        scene_dict, _ = scenes
        mgr = SceneMgr(scene_dict, 30)
        with pytest.raises(KeyError):
            mgr.current_scene.remove_scene("nonexistent")

    def test_enter_default_pass(self, scenes, screen):
        """The base Scene.enter() should be a pass."""
        scene_dict, _ = scenes
        mgr = SceneMgr(scene_dict, 30)
        scene_b = scene_dict["B"]
        # B doesn't override enter(), so default should be used
        scene_b.enter()  # should not raise

    def test_leave_default_pass(self, scenes, screen):
        """The base Scene.leave() should be a pass."""
        scene_dict, _ = scenes
        SceneMgr(scene_dict, 30)
        scene_b = scene_dict["B"]
        scene_b.leave()  # should not raise

    def test_scene_has_scene_mgr_ref(self, scenes, screen):
        scene_dict, _ = scenes
        mgr = SceneMgr(scene_dict, 30)
        assert scene_dict["A"].scene_mgr is mgr
        assert scene_dict["B"].scene_mgr is mgr
