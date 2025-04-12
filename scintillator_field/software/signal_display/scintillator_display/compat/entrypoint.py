from scintillator_display.display.impl_a.app import App as IMPL_A
from scintillator_display.compat.viewport_manager import ViewportManager

def entrypoint():
    vm = ViewportManager()

    impl_a = IMPL_A((1280, 720), "IMPL_A")
    vp_a = impl_a.window

    def impl_a_render():
        impl_a.on_render_frame()
        impl_a.ui.on_render_ui(impl_a.window, impl_a.pt_selected)

    vm.set_on_render(vp_a, impl_a_render)

    vm.render_loop()
