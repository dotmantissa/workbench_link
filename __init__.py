"""Directory-plugin entrypoint. Registration never starts a service."""

from .workbench_link.plugin import register

__all__ = ['register']
