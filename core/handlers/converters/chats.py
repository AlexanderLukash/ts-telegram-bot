from core.dtos.messages import ChatListItemDTO


def convert_chat_dtos_to_message(chats: list[ChatListItemDTO]) -> str:
    return "\n".join(
        (
            "List of all the chats available:",
            "\n".join(
                f"ChatOID: {chat.oid}, \nProblem: {chat.title}" for chat in chats
            ),
        ),
    )
