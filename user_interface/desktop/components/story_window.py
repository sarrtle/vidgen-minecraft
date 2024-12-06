"""The sidebar content of story section from the sidebar."""

from PIL import Image
from customtkinter import (
    CTkButton,
    CTkComboBox,
    CTkEntry,
    CTkFont,
    CTkFrame,
    CTkImage,
    CTkLabel,
    CTkScrollableFrame,
    CTkTextbox,
    Variable,
)

from tkinter import messagebox

from typing import Any, Literal

from models.config_data import ConfigData
from models.story_window_model import StoryWindowValues
from utility.config_tools import save_api_config


class StoryWindow(CTkFrame):
    """Story window contents."""

    def __init__(self, master: CTkFrame, config_data: ConfigData, **kwargs: Any):
        """Initialize story window.

        Args:
            master (customtkinter.CTkFrame): The main window of the Desktop.
            config_data (models.config_data.ConfigData): For saving and loading configurations
            **kwargs (Any): What CTkFrame needs.

        Notes:
            Any changes made when packing or rendering the
            component or widget are done on method:
            `StoryWindow.render`.

            This component has 2 containers. The left one is
            the preview image and the right one is the video
            settings.

        """
        super().__init__(master, **kwargs)

        # important variables
        self._config_data: ConfigData = config_data
        self._story_widows_values: StoryWindowValues | None = None

        # values get and set
        self._theme_variable: Variable = Variable(value="Horror")
        self._text_model_variable: Variable = Variable(value="DeepInfra")
        self._idea_entry: CTkEntry | None = None
        self._context_textbox: CTkTextbox | None = None
        self._voice_model_variable: Variable = Variable(value="Arceus")
        self._text_position_variable: Variable = Variable(value="center")
        self._text_font_variable: Variable = Variable(value="default")

        # left and right container
        self._left_side_container: CTkFrame | None = None
        self._right_side_container: CTkFrame | None = None

        # image preview widget
        self._image_preview_widget: CTkLabel | None = None

        # setup important functions
        self._setup_containers()

    def _setup_containers(self):
        """Set up the preview and control options for Story window."""
        self._left_side_container = CTkFrame(master=self)
        self._left_side_container.pack(fill="both", side="left")
        scrollable_right_side_container = CTkScrollableFrame(
            master=self, fg_color="transparent"
        )
        scrollable_right_side_container.pack(fill="both", expand=True)
        self._right_side_container = CTkFrame(
            master=scrollable_right_side_container, fg_color="transparent"
        )
        self._right_side_container.pack(
            fill="both", expand=True, padx=24, pady=(24, 16)
        )

        CTkButton(master=self, text="Render Video").pack(
            anchor="e", padx=24, pady=(8, 16)
        )

        # load image preview
        default_image = Image.open("assets/preview/default.png")
        self._image_preview_widget = CTkLabel(
            master=self._left_side_container,
            text="Preview",
            image=CTkImage(
                light_image=default_image, dark_image=default_image, size=(360, 640)
            ),
        )
        self._image_preview_widget.pack(anchor="center", expand=True, padx=32)

        self._setup_settings_and_options()

    def _setup_settings_and_options(self):
        """Set up settings and options.

        Here are the list of widget functions that are
        use to set them up.
        """
        self._setup_theme_text_model()
        self._setup_idea_context_settings()
        self._setup_preview_voiceover_settings()
        self._setup_video_options_settings()

    def _setup_theme_text_model(self):
        """Set up theme and text model widgets."""
        # Theme
        theme_text_model_frame = CTkFrame(master=self._right_side_container)
        theme_text_model_frame.pack(fill="x", expand=True)
        theme_frame = CTkFrame(master=theme_text_model_frame, fg_color="transparent")
        theme_frame.pack(fill="x", expand=True)
        CTkLabel(
            master=theme_frame, text="Theme", font=self._get_font(16, "bold")
        ).pack(side="left", anchor="w", padx=16, pady=16)
        CTkComboBox(
            master=theme_frame,
            values=["Horror", "Facts"],
            variable=self._theme_variable,
            command=lambda _: self._save_story_settings_to_config(),
        ).pack(anchor="e", padx=16, pady=16)
        self._theme_variable.set(value=self._config_data.story_settings.theme)

        # AI model
        # use theme text model frame since they are group
        ai_model_frame = CTkFrame(master=theme_text_model_frame, fg_color="transparent")
        ai_model_frame.pack(fill="x", expand=True)
        CTkLabel(
            master=ai_model_frame, text="Text Model", font=self._get_font(16, "bold")
        ).pack(side="left", anchor="w", padx=16, pady=(0, 16))
        CTkComboBox(
            master=ai_model_frame,
            values=[
                "DeepInfra",
                "Openai",
            ],
            variable=self._text_model_variable,
            command=lambda _: self._save_story_settings_to_config(),
        ).pack(anchor="e", padx=16, pady=(0, 16))
        self._text_model_variable.set(value=self._config_data.story_settings.text_model)

    def _setup_idea_context_settings(self):
        """Set up generate from idea and edit context widgets."""
        # Idea
        idea_context_frame = CTkFrame(master=self._right_side_container)
        idea_context_frame.pack(fill="x", expand=True, pady=20)
        idea_frame = CTkFrame(master=idea_context_frame, fg_color="transparent")
        idea_frame.pack(fill="x", expand=True)
        CTkLabel(
            master=idea_frame,
            text="Idea",
            font=self._get_font(16, "bold"),
        ).pack(anchor="w", padx=16, pady=(16, 8))
        self._idea_entry = CTkEntry(
            master=idea_context_frame,
            placeholder_text="Tell me your idea.",
        )
        self._idea_entry.pack(fill="x", padx=16, pady=(0, 8))
        CTkButton(
            master=idea_context_frame, text="Generate", command=self._on_generate_idea
        ).pack(anchor="e", padx=16, pady=(0, 8))

        # Context
        CTkLabel(
            master=idea_context_frame, text="Context", font=self._get_font(16, "bold")
        ).pack(anchor="w", padx=16)
        CTkLabel(
            master=idea_context_frame,
            text="Paste if you have an already made content or feel free to edit from the generated idea.",
            font=self._get_font(12, "normal"),
        ).pack(anchor="w", padx=16, pady=(0, 8))
        self._context_textbox = CTkTextbox(master=idea_context_frame)
        self._context_textbox.pack(fill="x", padx=16, pady=(0, 16))

    def _setup_preview_voiceover_settings(self):
        """Set up preview voiceover widgets."""
        # Preview voiceover
        preview_voiceover_frame = CTkFrame(master=self._right_side_container)
        preview_voiceover_frame.pack(fill="x", expand=True, pady=(0, 20))
        voice_model_frame = CTkFrame(preview_voiceover_frame, fg_color="transparent")
        voice_model_frame.pack(fill="x", expand=True)
        CTkLabel(
            master=voice_model_frame,
            text="Voice model",
            font=self._get_font(16, "bold"),
        ).pack(side="left", anchor="w", padx=16, pady=16)
        CTkComboBox(
            master=voice_model_frame,
            values=["Arceus", "Luna", "Asteria"],
            font=self._get_font(),
            variable=self._voice_model_variable,
            command=lambda _: self._save_story_settings_to_config(),
        ).pack(anchor="e", padx=16, pady=(16, 0))
        self._voice_model_variable.set(
            value=self._config_data.story_settings.voice_model
        )
        CTkButton(master=voice_model_frame, text="Play").pack(
            anchor="e", padx=16, pady=(8, 16)
        )

    def _setup_video_options_settings(self):
        """Set up video options widgets."""
        # video options
        video_options_frame = CTkFrame(master=self._right_side_container)
        video_options_frame.pack(fill="x", expand=True)

        # clips
        clips_frame = CTkFrame(master=video_options_frame, fg_color="transparent")
        clips_frame.pack(fill="x", expand=True)
        CTkLabel(
            master=clips_frame, text="Clips", font=self._get_font(16, "bold")
        ).pack(anchor="w", side="left", padx=16, pady=16)
        CTkButton(master=clips_frame, text="browse").pack(anchor="e", padx=16, pady=16)

        # randomize position
        randomize_frame = CTkFrame(master=video_options_frame, fg_color="transparent")
        randomize_frame.pack(fill="x", expand=True)
        CTkLabel(
            master=randomize_frame,
            text="Randomize position",
            font=self._get_font(16, "bold"),
        ).pack(side="left", anchor="w", padx=16, pady=(0, 16))
        CTkButton(master=randomize_frame, text="randomize").pack(
            anchor="e", padx=16, pady=(0, 16)
        )

        # text position
        text_position_frame = CTkFrame(
            master=video_options_frame, fg_color="transparent"
        )
        text_position_frame.pack(fill="x", expand=True)
        CTkLabel(
            master=text_position_frame,
            text="Text position",
            font=self._get_font(16, "bold"),
        ).pack(side="left", anchor="w", padx=16, pady=(0, 16))
        CTkComboBox(
            master=text_position_frame,
            values=["top", "center", "bottom"],
            font=self._get_font(),
            variable=self._text_position_variable,
            command=lambda _: self._save_story_settings_to_config(),
        ).pack(anchor="e", padx=16, pady=(0, 16))
        self._text_position_variable.set(
            value=self._config_data.story_settings.text_position
        )

        # text font
        text_font_frame = CTkFrame(master=video_options_frame, fg_color="transparent")
        text_font_frame.pack(fill="x", expand=True)
        CTkLabel(
            master=text_font_frame,
            text="Text font",
            font=self._get_font(16, "bold"),
        ).pack(side="left", anchor="w", padx=16, pady=(0, 16))
        CTkComboBox(
            master=text_font_frame,
            values=["default", "Futura", "Monosans"],
            font=self._get_font(),
            variable=self._text_font_variable,
            command=lambda _: self._save_story_settings_to_config(),
        ).pack(anchor="e", padx=16, pady=(0, 16))
        self._text_font_variable.set(value=self._config_data.story_settings.font)

    def _get_font(self, size: int = 14, weight: Literal["normal", "bold"] = "normal"):
        """Create font.

        TODO: Make this as a utility.
        """
        return CTkFont("assets/fonts/futura-extra-bold.ttf", size=size, weight=weight)

    def _get_idea_entry_value(self):
        """Get the value of entry from idea entry."""
        if self._idea_entry:
            return self._idea_entry.get()

        return ""

    def _get_context_textbox_value(self):
        """Get the valuue of text box from context."""
        if self._context_textbox:
            return self._context_textbox.get("1.0", "end-1c")

        return ""

    def _get_all_values(self):
        """Get all values from the story window settings."""
        return StoryWindowValues(
            theme=self._theme_variable.get(),
            text_model=self._text_model_variable.get(),
            idea=self._get_idea_entry_value(),
            context=self._get_context_textbox_value(),
            voice_model=self._voice_model_variable.get(),
            text_position=self._text_position_variable.get(),
            text_font=self._text_font_variable.get(),
        )

    def _save_story_settings_to_config(self):
        """Save story settings to `config.json` local file."""
        story_windows_values = self._get_all_values()

        # save story settings data on config
        self._config_data.story_settings.theme = story_windows_values.theme
        self._config_data.story_settings.text_model = story_windows_values.text_model
        self._config_data.story_settings.voice_model = story_windows_values.voice_model
        self._config_data.story_settings.font = story_windows_values.text_font
        self._config_data.story_settings.text_position = (
            story_windows_values.text_position
        )

        save_api_config(config_object=self._config_data)

    # Button commands
    def _on_generate_idea(self):
        idea_string = self._get_idea_entry_value()

        if not idea_string:
            messagebox.showwarning(
                title="No Idea!",
                message="Please input some idea before clicking generate.",
            )

    def render(self):
        """Render the component to the main window."""
        self.pack(expand=True, fill="both", side="left", anchor="w")
