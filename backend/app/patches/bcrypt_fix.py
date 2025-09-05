import bcrypt
import logging
logger = logging.getLogger("app")

def patch_bcrypt():
    """Патч для исправления ошибки passlib"""
    if not hasattr(bcrypt, '__about__'):
        class MockAbout:
            __version__ = bcrypt.__version__
        
        bcrypt.__about__ = MockAbout()
    print(1)
    logger.info(f"✅ BCrypt patched: {bcrypt.__version__}")

# Вызываем патч при импорте
patch_bcrypt()