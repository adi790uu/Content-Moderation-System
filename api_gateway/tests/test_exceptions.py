import pytest
from app.core.exceptions import ServiceException, ValidationException


def test_service_exception():
    with pytest.raises(ServiceException):
        raise ServiceException("Test exception", status_code=400)


def test_validation_exception():
    with pytest.raises(ValidationException):
        raise ValidationException("Validation error", status_code=400)
