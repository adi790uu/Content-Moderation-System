import pytest
from app.core.exceptions import ServiceException, RepositoryException


def test_service_exception():
    with pytest.raises(ServiceException):
        raise ServiceException("Test exception", status_code=400)


def test_repository_exception():
    with pytest.raises(RepositoryException):
        raise RepositoryException("Repository error", status_code=404)
