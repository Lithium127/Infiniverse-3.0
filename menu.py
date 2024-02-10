import sys

from asciimatics.exceptions import ResizeScreenError, NextScene
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics import widgets as w

from assets import StaticObject, START_OBJECT



class StaticAssetView(w.Frame):
    
    _current_asset: StaticObject
    
    def __init__(self, screen: Screen, start_asset: StaticObject) -> None:
        super(StaticAssetView, self).__init__(
            screen,
            screen.height * 2//3,
            screen.width * 2//3,
            on_load = self._reload,
            hover_focus = True,
            title = "Infiniverse 3.0"
        )
        
        self._current_asset = start_asset
        
        # Object and Content view
        self._layout_objects = w.Layout([39, 2, 59], fill_frame=True)
        self.add_layout(self._layout_objects)
        
        self._listbox_content = w.ListBox(
            w.Widget.FILL_COLUMN,
            [("No asset data", None)],
            add_scroll_bar= True,
            on_select = self._on_content_select
        )
        
        self._asset_name = w.Text("Name:", readonly=True, disabled=True)
        self._asset_class = w.Text("Class:", readonly=True, disabled=True)
        self._asset_content_len = w.Text("Len:", readonly=True, disabled=True)
        self._asset_description = w.TextBox(w.Widget.FILL_COLUMN, readonly=True, disabled=True)
        
        self._layout_objects.add_widget(self._asset_name, 0)
        self._layout_objects.add_widget(self._asset_class, 0)
        self._layout_objects.add_widget(self._asset_content_len, 0)
        self._layout_objects.add_widget(w.Divider())
        self._layout_objects.add_widget(self._asset_description, 0)
        
        self._layout_objects.add_widget(w.VerticalDivider(), 1)
        
        self._layout_objects.add_widget(w.Label("Contents"), 2)
        self._layout_objects.add_widget(w.Divider(), 2)
        self._layout_objects.add_widget(self._listbox_content, 2)
        
        # Action Layout
        self._layout_actions = w.Layout([1,1,1])
        self.add_layout(self._layout_actions)
        
        self._button_back = w.Button("Back", on_click=self._back)
        self._button_select = w.Button("Select", on_click=self._select)
        
        self._layout_actions.add_widget(self._button_back, 0)
        self._layout_actions.add_widget(self._button_select, 2)
        
        self.fix()
    
    def _reload(self) -> None:
        self._current_asset.generate()
        
        # regenerate listbox options
        self._listbox_content.options = self._current_asset._content_tuple
        self._update_dynamic_data()
        
        self._button_back.disabled = self._current_asset._parent is None
        self._button_select.disabled = self._listbox_content.value is None
        
    def _update_dynamic_data(self) -> None:
        self._asset_name._value = self._current_asset.name
        self._asset_class._value = self._current_asset.__class__.__name__
        self._asset_content_len._value = str(len(self._current_asset._contents))
        
        self._asset_description._value = [""]
        
        lines = self._current_asset._dynamic_display()
        if lines is None:
            return
        data = []
        for line, value in lines:
            data.append(f"{line} : {value}")
    
    def _back(self) -> None:
        if self._current_asset._parent is not None:
            self._current_asset = self._current_asset._parent
            raise NextScene("object_view")
    
    def _select(self) -> None:
        if self._listbox_content._value is not None:
            # possibly switch to index system to have asset handle child selection
            self._current_asset = self._listbox_content._value
            raise NextScene("object_view")
    
    def _on_content_select(self) -> None:
        self._button_select.disabled = self._listbox_content.value is None


def wrapped_UI(screen, scene):
    # Define your Scenes here
    scenes = [
        Scene([StaticAssetView(screen, START_OBJECT)], -1, name="object_view")
    ]

    # Run your program
    screen.play(scenes, stop_on_resize=True, start_scene=scene)


def start_UI():
    last_scene = None
    while True:
        try:
            Screen.wrapper(wrapped_UI, arguments=[last_scene])
            sys.exit(0)
        except ResizeScreenError as e:
            last_scene = e.scene