from app import dao
from app.models import dto


async def upsert_user_chat(user: dto.User, chat: dto.Chat, holder: dao.HolderDao):
    await holder.chat.add_user(chat, user)
    await holder.commit()
