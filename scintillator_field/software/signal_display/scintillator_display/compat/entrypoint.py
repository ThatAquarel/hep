from scintillator_display.compat.viewport_manager import ViewportManager

from scintillator_display.display.impl_controls.controls import Controls
from scintillator_display.display.impl_a.app import App as IMPL_A
from scintillator_display.display.impl_b.window import Window as IMPL_B


def entrypoint():
    vm = ViewportManager()

    impl_controls = Controls()
    vp_controls = impl_controls.window

    vm.set_vp_ratio(vp_controls, 1)
    vm.set_on_render(vp_controls, impl_controls.on_render)


    impl_a = IMPL_A((1, 1), "IMPL_A")
    vp_a = impl_a.window

    def impl_a_render():
        impl_a.on_render_frame()
        impl_a.ui.on_render_ui(impl_a.window, impl_a.pt_selected)

    vm.set_vp_ratio(vp_a, 2)
    vm.set_on_render(vp_a, impl_a_render)


    impl_b = IMPL_B()
    impl_b.main()
    vp_b = impl_b.window

    def impl_b_render():
        impl_b.render_loop()

    vm.set_vp_ratio(vp_b, 2)
    vm.set_on_render(vp_b, impl_b_render)


    vm.render_loop()
