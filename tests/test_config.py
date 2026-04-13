from app.config import Settings


def test_public_settings_mask_secrets() -> None:
    settings = Settings(google_api_key="secret")

    public_settings = settings.as_public_dict()

    assert public_settings["google_api_key"] == "configured"
