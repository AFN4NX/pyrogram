#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from typing import Optional, List

from pyrogram import raw, types, utils
from ..object import Object


class GiftCode(Object):
    """Contains gift code data.

    Parameters:
        months (``int``):
            Number of months of subscription.

        slug (``str``):
            Identifier of gift code.
            You can combine it with `t.me/giftcode/{slug}`
            to get link for this gift.

        text (``str``, *optional*):
            Text message.

        entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
            For text messages, special entities like usernames, URLs, bot commands, etc. that appear in the text.

        via_giveaway (``bool``, *optional*):
            True if the gift code is received via giveaway.

        is_unclaimed (``bool``, *optional*):
            True if the winner for the corresponding Telegram Premium subscription wasn't chosen.

        boosted_chat (:obj:`~pyrogram.types.Chat`, *optional*):
            The channel where the gift code was won.

        link (``str``, *property*):
            Generate a link to this gift code.
    """

    def __init__(
        self,
        *,
        months: int,
        slug: str,
        text: Optional[str] = None,
        entities: List["types.MessageEntity"] = None,
        via_giveaway: Optional[bool] = None,
        is_unclaimed: Optional[bool] = None,
        boosted_chat: Optional["types.Chat"] = None
    ):
        super().__init__()

        self.months = months
        self.slug = slug
        self.text = text
        self.entities = entities
        self.via_giveaway = via_giveaway
        self.is_unclaimed = is_unclaimed
        self.boosted_chat = boosted_chat

    @staticmethod
    def _parse(client, giftcode: "raw.types.MessageActionGiftCode", users, chats):
        peer = chats.get(utils.get_raw_peer_id(getattr(giftcode, "boost_peer")))

        return GiftCode(
            months=giftcode.months,
            slug=giftcode.slug,
            via_giveaway=getattr(giftcode, "via_giveaway"),
            is_unclaimed=getattr(giftcode, "unclaimed"),
            boosted_chat=types.Chat._parse_chat(client, peer) if peer else None,
            **utils.parse_text_with_entities(client, getattr(giftcode, "message", None), users)
        )

    @property
    def link(self) -> str:
        return f"https://t.me/giftcode/{self.slug}"
