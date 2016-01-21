__author__ = 'Colin'


def test_alter_get():
    from dispatch import Dispatch
    from dispatch.profiles import profile_registry

    def foo_clock_skew():
        return 20

    profile_registry.get_profile("Arista").add_getter("ntp.client.skew", foo_clock_skew)

    dispatcher = Dispatch()

    device = dispatcher.connect("switch01")
    device.get("ntp.client.skew")
