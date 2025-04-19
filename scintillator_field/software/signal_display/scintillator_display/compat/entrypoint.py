from scintillator_display.compat.viewport_manager import ViewportManager

from scintillator_display.display.impl_controls.controls import Controls
from scintillator_display.display.impl_a.app import App as IMPL_A
from scintillator_display.display.impl_b.window import Window as IMPL_B


def entrypoint():
    vm = ViewportManager()

    ratio = [1, 2, 2]

    impl_controls = Controls()
    impl_a = IMPL_A((1, 1))
    impl_b = IMPL_B()
    impl_controls.impl_a = impl_a
    impl_controls.impl_b = impl_b


    # impl controls
    vp_controls = impl_controls.window

    vm.set_vp_ratio(vp_controls, ratio[0])
    vm.set_on_render(vp_controls, impl_controls.on_render)


    # impl_a
    vp_a = impl_a.window

    def impl_a_render():
        impl_a.on_render_frame()

    vm.set_vp_ratio(vp_a, ratio[1])
    vm.set_on_render(vp_a, impl_a_render)


    # impl_b
    impl_b.main()
    vp_b = impl_b.window

    def impl_b_render():
        impl_b.render_loop()

    vm.set_vp_ratio(vp_b, ratio[2])
    vm.set_on_render(vp_b, impl_b_render)

    
    impl_controls.activate_data_connection()

    vm.render_loop()
