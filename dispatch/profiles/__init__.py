import copy
import logging
import socket

from dispatch.exceptions import (
    DispatchMissingParameter,
    DispatchNoProfileMatched,
    DispatchProfileNotFound,
    EXC_DOT_IN_NAME,
    EXC_COLON_IN_NAME,
    EXC_NOT_PROFILE_OBJECT
)


logger = logging.getLogger("dispatch.profiles")


profile_registry = {}
profile_identifiers = {}


class Profile(object):
    """Profile"""

    def __init__(self):
        self.getters = []
        self.setters = []


class Device(object):
    """Device"""

    def __init__(self, name, ip_address, profile, discover_profile_now=False):
        self.name = name
        self.ip_address = ip_address or socket.gethostbyname(self.name)
        self._profile = profile

    def discover_driver(self):
        matched_profiles = []
        for profile_name, profile_definition in profile_registry.items():
            if profile_definition.match(self):
                logger.debug("Matched a device to a profile. Device='{}' Profile='{}'".format(self.name, profile_name))
                matched_profiles.append(profile_definition)
        if not matched_profiles:
            logger.error("Unable to match a profile for device '{}'".format(self.name))
            raise DispatchNoProfileMatched("Unable to match a profile for device '{}'".format(self.name))
        self.profile = compile_profile_definitions(matched_profiles)

    @property
    def profile(self):
        if self._profile is None:
            logger.info("No profile specified for {}. Starting profile discovery.".format(self.name))
            self.discover_driver()
        return self._profile

    @profile.setter
    def profile(self, profile):
        assert isinstance(profile, Profile), EXC_NOT_PROFILE_OBJECT
        self._profile = profile

    def set_profile(self, profile=None, profile_name=None):
        if profile_name:
            if profile_name not in profile_registry.keys():
                raise DispatchProfileNotFound(profile_name)
            self._profile = profile_registry[profile_name]
        elif profile:
            self.profile = profile
        else:
            raise DispatchMissingParameter("Missing either 'profile' or 'profile_name' parameter.")

    def get(self, parameter):
        profile = profile_registry[self.profile]
        for getter_name, getter_func in profile.getters:
            if getter_name == parameter:
                return getter_func(self)

    def set(self, parameter, value):
        profile = profile_registry[self.profile]
        for setter_name, setter_func in profile.setters.items():
            if setter_name == parameter:
                return setter_func(self, value)


class ProfileDefinition(object):

    def __init__(self, profile_name):
        assert ":" not in profile_name, EXC_COLON_IN_NAME
        assert "." not in profile_name, EXC_DOT_IN_NAME

        self.profile_name = profile_name

        self.includes = {}
        self.excludes = {}

        self.getters = {}
        self.setters = {}
        self.identifiers = {}
    
    def add_getter(self, name, func):
        """Adds a getter to the ProfileDefinition."""
        self.getters[name] = func
    
    def add_setter(self, name, func):
        """Adds a setter to the ProfileDefinition."""
        self.setters[name] = func
    
    def add_identifier(self, name, func):
        """Adds a setter to the ProfileDefinition."""
        self.identifiers[name] = func
    
    def gets(self, name):
        """Decorator alias for ProfileDefinition.add_getter()."""
        def decorator(func):
            self.getters[name] = func
            return func
        return decorator
    
    def sets(self, name):
        """Decorator alias for ProfileDefinition.add_setter()."""
        def decorator(func):
            self.setters[name] = func
            return func
        return decorator

    def identifies(self, name):
        """Decorator alias for ProfileDefinition.add_identifier()."""
        def decorator(func):
            self.identifiers[name] = func
            return func
        return decorator

    def match(self, device):
        for identifier_name, identifier_func in self.identifiers.items():
            logger.debug("Running profile '{}' identifier '{}' on device '{}'".format(self.profile_name,
                                                                                      identifier_name,
                                                                                      device.name))
            if not identifier_func(device):
                logger.debug("Profile '{}' identifier '{}' did not pass for device '{}'".format(self.profile_name,
                                                                                                identifier_name,
                                                                                                device.name))
                return False
        logger.debug("Profile '{}' matched device '{}'".format(self.profile_name, device.name))
        return True


def define_profile(name, includes=None, excludes=None):
    """Create a new device profile.

    This function automatically generates a new class for each profile and stores
    it in the profile_registry.

    Parameters:
        name		(string)	: A string that will be the resulting class name.
        include 	(list)		: A list of of other profile classes or methods that will be available in this profile.

    """
    profile_definition = ProfileDefinition(name)

    profile_definition.includes = includes or {}
    profile_definition.excludes = excludes or {}

    profile_registry[name] = profile_definition
    return profile_definition


def resolve_includes(includes, excludes):
    resolved = {}
    for include_name in includes:
        if "." in include_name:     # This means it's a method off another profile
            include_profile_name, include_method_name = include_name.lsplit(".", 1)
            include_profile = profile_registry[include_profile_name]
            include_method = include_profile.getters[include_method_name]
            if not any(name in excludes for name in (include_name, include_profile_name, include_method_name)):
                resolved[include_method_name] = copy.deepcopy(include_method)
        else:   # This is a whole profile
            include_profile = profile_registry[include_name]
    return resolved


def compile_profile_definitions(profile_definitions):
    includes = []
    excludes = []
    getters = []
    setters = []

    for definition in profile_definitions:

