# -*- coding: utf-8 -*-

from typing import Callable, List, Optional

try:
    import ujson as json
except ImportError:
    import json

import six

from telebot import util, logger


class JsonSerializable:
    """
    Subclasses of this class are guaranteed to be able to be converted to JSON format.
    All subclasses of this class must override to_json.
    """

    def to_json(self):
        """
        Returns a JSON string representation of this class.

        This function must be overridden by subclasses.
        :return: a JSON formatted string.
        """
        raise NotImplementedError


class Dictionaryable:
    """
    Subclasses of this class are guaranteed to be able to be converted to dictionary.
    All subclasses of this class must override to_dic.
    """

    def to_dic(self):
        """
        Returns a JSON string representation of this class.

        This function must be overridden by subclasses.
        :return: a JSON formatted string.
        """
        raise NotImplementedError


class JsonDeserializable:
    """
    Subclasses of this class are guaranteed to be able to be created from a json-style dict or json formatted string.
    All subclasses of this class must override de_json.
    """

    @classmethod
    def de_json(cls, json_type):
        """
        Returns an instance of this class from the given json dict or string.

        This function must be overridden by subclasses.
        :return: an instance of this class created from the given json dict or string.
        """
        raise NotImplementedError

    @staticmethod
    def check_json(json_type, dict_copy = True):
        """
        Checks whether json_type is a dict or a string. If it is already a dict, it is returned as-is.
        If it is not, it is converted to a dict by means of json.loads(json_type)
        :meta private:

        :param json_type: input json or parsed dict
        :param dict_copy: if dict is passed and it is changed outside - should be True!
        :return: Dictionary parsed from json or original dict
        """
        if util.is_dict(json_type):
            return json_type.copy() if dict_copy else json_type
        elif util.is_string(json_type):
            return json.loads(json_type)
        else:
            raise ValueError("json_type should be a json dict or string.")

    def __str__(self):
        d = {
            x: y.__dict__ if hasattr(y, '__dict__') else y
            for x, y in self.__dict__.items()
        }
        return str(d)


class Update(JsonDeserializable):
    @classmethod
    def de_json(cls, json_type):
        logger.debug('Update.de_json: %s', json_type)
        obj = cls.check_json(json_type)
        update_id = obj['update_id']
        message = None
        edited_message = None
        channel_post = None
        edited_channel_post = None
        inline_query = None
        chosen_inline_result = None
        callback_query = None
        shipping_query = None
        pre_checkout_query = None
        poll = None
        poll_answer = None
        if 'message' in obj:
            message = Message.de_json(obj['message'])
        if 'edited_message' in obj:
            edited_message = Message.de_json(obj['edited_message'])
        if 'channel_post' in obj:
            channel_post = Message.de_json(obj['channel_post'])
        if 'edited_channel_post' in obj:
            edited_channel_post = Message.de_json(obj['edited_channel_post'])
        if 'inline_query' in obj:
            inline_query = InlineQuery.de_json(obj['inline_query'])
        if 'chosen_inline_result' in obj:
            chosen_inline_result = ChosenInlineResult.de_json(obj['chosen_inline_result'])
        if 'callback_query' in obj:
            callback_query = CallbackQuery.de_json(obj['callback_query'])
        if 'shipping_query' in obj:
            shipping_query = ShippingQuery.de_json(obj['shipping_query'])
        if 'pre_checkout_query' in obj:
            pre_checkout_query = PreCheckoutQuery.de_json(obj['pre_checkout_query'])
        if 'poll' in obj:
            poll = Poll.de_json(obj.get('poll'))
        if 'poll_answer' in obj:
            poll_answer = PollAnswer.de_json(obj.get('poll_answer'))
        return cls(update_id, message, edited_message, channel_post, edited_channel_post, inline_query,
                   chosen_inline_result, callback_query, shipping_query, pre_checkout_query, poll, poll_answer)

    def __init__(self, update_id, message, edited_message, channel_post, edited_channel_post, inline_query,
                 chosen_inline_result, callback_query, shipping_query, pre_checkout_query, poll, poll_answer):
        self.update_id = update_id
        self.edited_message = edited_message
        self.message = message
        self.edited_message = edited_message
        self.channel_post = channel_post
        self.edited_channel_post = edited_channel_post
        self.inline_query = inline_query
        self.chosen_inline_result = chosen_inline_result
        self.callback_query = callback_query
        self.shipping_query = shipping_query
        self.pre_checkout_query = pre_checkout_query
        self.poll = poll
        self.poll_answer = poll_answer


class WebhookInfo(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        url = obj['url']
        has_custom_certificate = obj['has_custom_certificate']
        pending_update_count = obj['pending_update_count']
        last_error_date = None
        last_error_message = None
        max_connections = None
        allowed_updates = None
        if 'last_error_message' in obj:
            last_error_date = obj['last_error_date']
        if 'last_error_message' in obj:
            last_error_message = obj['last_error_message']
        if 'max_connections' in obj:
            max_connections = obj['max_connections']
        if 'allowed_updates' in obj:
            allowed_updates = obj['allowed_updates']
        return cls(url, has_custom_certificate, pending_update_count, last_error_date, last_error_message,
                   max_connections, allowed_updates)

    def __init__(self, url, has_custom_certificate, pending_update_count, last_error_date, last_error_message,
                 max_connections, allowed_updates):
        self.url = url
        self.has_custom_certificate = has_custom_certificate
        self.pending_update_count = pending_update_count
        self.last_error_date = last_error_date
        self.last_error_message = last_error_message
        self.max_connections = max_connections
        self.allowed_updates = allowed_updates


class User(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        id = obj['id']
        is_bot = obj['is_bot']
        first_name = obj['first_name']
        last_name = obj.get('last_name')
        username = obj.get('username')
        language_code = obj.get('language_code')
        return cls(id, is_bot, first_name, last_name, username, language_code)

    def __init__(self, id, is_bot, first_name, last_name=None, username=None, language_code=None):
        self.id = id
        self.is_bot = is_bot
        self.first_name = first_name
        self.username = username
        self.last_name = last_name
        self.language_code = language_code


class GroupChat(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        id = obj['id']
        title = obj['title']
        return cls(id, title)

    def __init__(self, id, title):
        self.id = id
        self.title = title


class Chat(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        id = obj['id']
        type = obj['type']
        title = obj.get('title')
        username = obj.get('username')
        first_name = obj.get('first_name')
        last_name = obj.get('last_name')
        all_members_are_administrators = obj.get('all_members_are_administrators')
        photo = None
        if 'photo' in obj:
            photo = ChatPhoto.de_json(obj['photo'])
        description = obj.get('description')
        invite_link = obj.get('invite_link')
        pinned_message = None
        if 'pinned_message' in obj:
            pinned_message = Message.de_json(obj['pinned_message'])
        sticker_set_name = obj.get('sticker_set_name')
        can_set_sticker_set = obj.get('can_set_sticker_set')
        return cls(id, type, title, username, first_name, last_name, all_members_are_administrators,
                   photo, description, invite_link, pinned_message, sticker_set_name, can_set_sticker_set)

    def __init__(self, id, type, title=None, username=None, first_name=None, last_name=None,
                 all_members_are_administrators=None, photo=None, description=None, invite_link=None,
                 pinned_message=None, sticker_set_name=None, can_set_sticker_set=None):
        self.type = type
        self.last_name = last_name
        self.first_name = first_name
        self.username = username
        self.id = id
        self.title = title
        self.all_members_are_administrators = all_members_are_administrators
        self.photo = photo
        self.description = description
        self.invite_link = invite_link
        self.pinned_message = pinned_message
        self.sticker_set_name = sticker_set_name
        self.can_set_sticker_set = can_set_sticker_set


class PollOption(JsonDeserializable):
    """
    This object contains information about one answer option in a poll.

    Telegram Documentation: https://core.telegram.org/bots/api#polloption

    :param text: Option text, 1-100 characters
    :type text: :obj:`str`

    :param voter_count: Number of users that voted for this option
    :type voter_count: :obj:`int`

    :return: Instance of the class
    :rtype: :class:`telebot.types.PollOption`
    """
    @classmethod
    def de_json(cls, json_string):
        if (json_string is None): return None
        obj = cls.check_json(json_string, dict_copy=False)
        return cls(**obj)

    def __init__(self, text, voter_count = 0, **kwargs):
        self.text: str = text
        self.voter_count: int = voter_count
    # Converted in _convert_poll_options
    # def to_json(self):
    #     # send_poll Option is a simple string: https://core.telegram.org/bots/api#sendpoll
    #     return json.dumps(self.text)


class Poll(JsonDeserializable):
    """
    This object contains information about a poll.

    Telegram Documentation: https://core.telegram.org/bots/api#poll

    :param id: Unique poll identifier
    :type id: :obj:`str`

    :param question: Poll question, 1-300 characters
    :type question: :obj:`str`

    :param options: List of poll options
    :type options: :obj:`list` of :class:`telebot.types.PollOption`

    :param total_voter_count: Total number of users that voted in the poll
    :type total_voter_count: :obj:`int`

    :param is_closed: True, if the poll is closed
    :type is_closed: :obj:`bool`

    :param is_anonymous: True, if the poll is anonymous
    :type is_anonymous: :obj:`bool`

    :param type: Poll type, currently can be “regular” or “quiz”
    :type type: :obj:`str`

    :param allows_multiple_answers: True, if the poll allows multiple answers
    :type allows_multiple_answers: :obj:`bool`

    :param correct_option_id: Optional. 0-based identifier of the correct answer option. Available only for polls in
        the quiz mode, which are closed, or was sent (not forwarded) by the bot or to the private chat with the bot.
    :type correct_option_id: :obj:`int`

    :param explanation: Optional. Text that is shown when a user chooses an incorrect answer or taps on the lamp icon in a
        quiz-style poll, 0-200 characters
    :type explanation: :obj:`str`

    :param explanation_entities: Optional. Special entities like usernames, URLs, bot commands, etc. that appear in
        the explanation
    :type explanation_entities: :obj:`list` of :class:`telebot.types.MessageEntity`

    :param open_period: Optional. Amount of time in seconds the poll will be active after creation
    :type open_period: :obj:`int`

    :param close_date: Optional. Point in time (Unix timestamp) when the poll will be automatically closed
    :type close_date: :obj:`int`

    :return: Instance of the class
    :rtype: :class:`telebot.types.Poll`
    """
    @classmethod
    def de_json(cls, json_string):
        if (json_string is None): return None
        obj = cls.check_json(json_string)
        obj['poll_id'] = obj.pop('id')
        options = []
        for opt in obj['options']:
            options.append(PollOption.de_json(opt))
        obj['options'] = options or None
        if 'explanation_entities' in obj:
            obj['explanation_entities'] = Message.parse_entities(obj['explanation_entities'])
        return cls(**obj)

    # noinspection PyShadowingBuiltins
    def __init__(
            self,
            question, options,
            poll_id=None, total_voter_count=None, is_closed=None, is_anonymous=None, type=None,
            allows_multiple_answers=None, correct_option_id=None, explanation=None, explanation_entities=None,
            open_period=None, close_date=None, poll_type=None, **kwargs):
        self.id: str = poll_id
        self.question: str = question
        self.options: List[PollOption] = options
        self.total_voter_count: int = total_voter_count
        self.is_closed: bool = is_closed
        self.is_anonymous: bool = is_anonymous
        self.type: str = type
        if poll_type is not None:
            # Wrong param name backward compatibility
            logger.warning("Poll: poll_type parameter is deprecated. Use type instead.")
            if type is None:
                self.type: str = poll_type
        self.allows_multiple_answers: bool = allows_multiple_answers
        self.correct_option_id: int = correct_option_id
        self.explanation: str = explanation
        self.explanation_entities: List[MessageEntity] = explanation_entities
        self.open_period: int = open_period
        self.close_date: int = close_date

    def add(self, option):
        """
        Add an option to the poll.

        :param option: Option to add
        :type option: :class:`telebot.types.PollOption` or :obj:`str`
        """
        if type(option) is PollOption:
            self.options.append(option)
        else:
            self.options.append(PollOption(option))


class PollAnswer(JsonSerializable, JsonDeserializable, Dictionaryable):
    """
    This object represents an answer of a user in a non-anonymous poll.

    Telegram Documentation: https://core.telegram.org/bots/api#pollanswer

    :param poll_id: Unique poll identifier
    :type poll_id: :obj:`str`

    :param user: The user, who changed the answer to the poll
    :type user: :class:`telebot.types.User`

    :param option_ids: 0-based identifiers of answer options, chosen by the user. May be empty if the user retracted
        their vote.
    :type option_ids: :obj:`list` of :obj:`int`

    :return: Instance of the class
    :rtype: :class:`telebot.types.PollAnswer`
    """
    @classmethod
    def de_json(cls, json_string):
        if (json_string is None): return None
        obj = cls.check_json(json_string)
        obj['user'] = User.de_json(obj['user'])
        return cls(**obj)

    def __init__(self, poll_id, user, option_ids, **kwargs):
        self.poll_id: str = poll_id
        self.user: User = user
        self.option_ids: List[int] = option_ids

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {'poll_id': self.poll_id,
                'user': self.user.to_dict(),
                'option_ids': self.option_ids}


class VideoChatStarted(JsonDeserializable):
    """
    This object represents a service message about a video chat started in the chat. Currently holds no information.
    """
    @classmethod
    def de_json(cls, json_string):
        return cls()

    def __init__(self):
        pass


class VoiceChatStarted(VideoChatStarted):
    """
    Deprecated, use :class:`VideoChatStarted` instead.
    """

    def __init__(self):
        logger.warning('VoiceChatStarted is deprecated. Use VideoChatStarted instead.')
        super().__init__()


class VideoChatScheduled(JsonDeserializable):
    """
    This object represents a service message about a video chat scheduled in the chat.
    Telegram Documentation: https://core.telegram.org/bots/api#videochatscheduled
    :param start_date: Point in time (Unix timestamp) when the video chat is supposed to be started by a chat
        administrator
    :type start_date: :obj:`int`
    :return: Instance of the class
    :rtype: :class:`telebot.types.VideoChatScheduled`
    """
    @classmethod
    def de_json(cls, json_string):
        if json_string is None: return None
        obj = cls.check_json(json_string, dict_copy=False)
        return cls(**obj)

    def __init__(self, start_date, **kwargs):
        self.start_date: int = start_date


class VoiceChatScheduled(VideoChatScheduled):
    """
    Deprecated, use :class:`VideoChatScheduled` instead.
    """
    def __init__(self, *args, **kwargs):
        logger.warning('VoiceChatScheduled is deprecated. Use VideoChatScheduled instead.')
        super().__init__(*args, **kwargs)


class VideoChatEnded(JsonDeserializable):
    """
    This object represents a service message about a video chat ended in the chat.
    Telegram Documentation: https://core.telegram.org/bots/api#videochatended
    :param duration: Video chat duration in seconds
    :type duration: :obj:`int`
    :return: Instance of the class
    :rtype: :class:`telebot.types.VideoChatEnded`
    """
    @classmethod
    def de_json(cls, json_string):
        if json_string is None: return None
        obj = cls.check_json(json_string, dict_copy=False)
        return cls(**obj)

    def __init__(self, duration, **kwargs):
        self.duration: int = duration


class VoiceChatEnded(VideoChatEnded):
    """
    Deprecated, use :class:`VideoChatEnded` instead.
    """
    def __init__(self, *args, **kwargs):
        logger.warning('VoiceChatEnded is deprecated. Use VideoChatEnded instead.')
        super().__init__(*args, **kwargs)


class VideoChatParticipantsInvited(JsonDeserializable):
    """
    This object represents a service message about new members invited to a video chat.
    Telegram Documentation: https://core.telegram.org/bots/api#videochatparticipantsinvited
    :param users: New members that were invited to the video chat
    :type users: :obj:`list` of :class:`telebot.types.User`
    :return: Instance of the class
    :rtype: :class:`telebot.types.VideoChatParticipantsInvited`
    """
    @classmethod
    def de_json(cls, json_string):
        if json_string is None: return None
        obj = cls.check_json(json_string)
        if 'users' in obj:
            obj['users'] = [User.de_json(u) for u in obj['users']]
        return cls(**obj)

    def __init__(self, users=None, **kwargs):
        self.users: List[User] = users


class VoiceChatParticipantsInvited(VideoChatParticipantsInvited):
    """
    Deprecated, use :class:`VideoChatParticipantsInvited` instead.
    """
    def __init__(self, *args, **kwargs):
        logger.warning('VoiceChatParticipantsInvited is deprecated. Use VideoChatParticipantsInvited instead.')
        super().__init__(*args, **kwargs)


class MenuButton(JsonDeserializable, JsonSerializable, Dictionaryable):
    """
    This object describes the bot's menu button in a private chat. It should be one of

    * :class:`MenuButtonCommands`
    * :class:`MenuButtonWebApp`
    * :class:`MenuButtonDefault`

    If a menu button other than MenuButtonDefault is set for a private chat, then it is applied
    in the chat. Otherwise the default menu button is applied. By default, the menu button opens the list of bot commands.
    """
    @classmethod
    def de_json(cls, json_string):
        if json_string is None: return None
        obj = cls.check_json(json_string)
        map = {
            'commands': MenuButtonCommands,
            'web_app': MenuButtonWebApp,
            'default': MenuButtonDefault
        }
        return map[obj['type']](**obj)

    def to_json(self):
        """
        :meta private:
        """
        raise NotImplementedError

    def to_dict(self):
        """
        :meta private:
        """
        raise NotImplementedError


class MenuButtonCommands(MenuButton):
    """
    Represents a menu button, which opens the bot's list of commands.

    Telegram Documentation: https://core.telegram.org/bots/api#menubuttoncommands

    :param type: Type of the button, must be commands
    :type type: :obj:`str`

    :return: Instance of the class
    :rtype: :class:`telebot.types.MenuButtonCommands`
    """

    def __init__(self, type):
        self.type = type

    def to_dict(self):
        return {'type': self.type}

    def to_json(self):
        return json.dumps(self.to_dict())


class MenuButtonWebApp(MenuButton):
    """
    Represents a menu button, which launches a Web App.

    Telegram Documentation: https://core.telegram.org/bots/api#menubuttonwebapp

    :param type: Type of the button, must be web_app
    :type type: :obj:`str`

    :param text: Text on the button
    :type text: :obj:`str`

    :param web_app: Description of the Web App that will be launched when the user presses the button. The Web App will be
        able to send an arbitrary message on behalf of the user using the method answerWebAppQuery.
    :type web_app: :class:`telebot.types.WebAppInfo`

    :return: Instance of the class
    :rtype: :class:`telebot.types.MenuButtonWebApp`
    """

    def __init__(self, type, text, web_app):
        self.type: str = type
        self.text: str = text
        self.web_app: WebAppInfo = web_app

    def to_dict(self):
        return {'type': self.type, 'text': self.text, 'web_app': self.web_app.to_dict()}

    def to_json(self):
        return json.dumps(self.to_dict())


class MenuButtonDefault(MenuButton):
    """
    Describes that no specific value for the menu button was set.

    Telegram Documentation: https://core.telegram.org/bots/api#menubuttondefault

    :param type: Type of the button, must be default
    :type type: :obj:`str`

    :return: Instance of the class
    :rtype: :class:`telebot.types.MenuButtonDefault`
    """
    def __init__(self, type):
        self.type: str = type

    def to_dict(self):
        return {'type': self.type}

    def to_json(self):
        return json.dumps(self.to_dict())


class WebAppData(JsonDeserializable, Dictionaryable):
    """
    Describes data sent from a Web App to the bot.

    Telegram Documentation: https://core.telegram.org/bots/api#webappdata

    :param data: The data. Be aware that a bad client can send arbitrary data in this field.
    :type data: :obj:`str`

    :param button_text: Text of the web_app keyboard button from which the Web App was opened. Be aware that a bad client
        can send arbitrary data in this field.
    :type button_text: :obj:`str`

    :return: Instance of the class
    :rtype: :class:`telebot.types.WebAppData`
    """

    def __init__(self, data, button_text):
        self.data = data
        self.button_text = button_text
    def to_dict(self):
        return {'data': self.data, 'button_text': self.button_text}

    @classmethod
    def de_json(cls, json_string):
        if json_string is None: return None
        obj = cls.check_json(json_string)
        return cls(**obj)


class Message(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        message_id = obj['message_id']
        from_user = None
        if 'from' in obj:
            from_user = User.de_json(obj['from'])
        date = obj['date']
        chat = Chat.de_json(obj['chat'])
        content_type = None
        opts = {}
        if 'forward_from' in obj:
            opts['forward_from'] = User.de_json(obj['forward_from'])
        if 'forward_from_chat' in obj:
            opts['forward_from_chat'] = Chat.de_json(obj['forward_from_chat'])
        if 'forward_from_message_id' in obj:
            opts['forward_from_message_id'] = obj.get('forward_from_message_id')
        if 'forward_signature' in obj:
            opts['forward_signature'] = obj.get('forward_signature')
        if 'forward_date' in obj:
            opts['forward_date'] = obj.get('forward_date')
        if 'reply_to_message' in obj:
            opts['reply_to_message'] = Message.de_json(obj['reply_to_message'])
        if 'edit_date' in obj:
            opts['edit_date'] = obj.get('edit_date')
        if 'author_signature' in obj:
            opts['author_signature'] = obj.get('author_signature')
        if 'text' in obj:
            opts['text'] = obj['text']
            content_type = 'text'
        if 'entities' in obj:
            opts['entities'] = Message.parse_entities(obj['entities'])
        if 'caption_entities' in obj:
            opts['caption_entities'] = Message.parse_entities(obj['caption_entities'])
        if 'audio' in obj:
            opts['audio'] = Audio.de_json(obj['audio'])
            content_type = 'audio'
        if 'document' in obj:
            opts['document'] = Document.de_json(obj['document'])
            content_type = 'document'
        if 'game' in obj:
            opts['game'] = Game.de_json(obj['game'])
            content_type = 'game'
        if 'photo' in obj:
            opts['photo'] = Message.parse_photo(obj['photo'])
            content_type = 'photo'
        if 'sticker' in obj:
            opts['sticker'] = Sticker.de_json(obj['sticker'])
            content_type = 'sticker'
        if 'video' in obj:
            opts['video'] = Video.de_json(obj['video'])
            content_type = 'video'
        if 'video_note' in obj:
            opts['video_note'] = VideoNote.de_json(obj['video_note'])
            content_type = 'video_note'
        if 'voice' in obj:
            opts['voice'] = Audio.de_json(obj['voice'])
            content_type = 'voice'
        if 'caption' in obj:
            opts['caption'] = obj['caption']
        if 'contact' in obj:
            opts['contact'] = Contact.de_json(json.dumps(obj['contact']))
            content_type = 'contact'
        if 'location' in obj:
            opts['location'] = Location.de_json(obj['location'])
            content_type = 'location'
        if 'venue' in obj:
            opts['venue'] = Venue.de_json(obj['venue'])
            content_type = 'venue'
        if 'new_chat_member' in obj:
            opts['new_chat_member'] = User.de_json(obj['new_chat_member'])
            content_type = 'new_chat_member'
        if 'new_chat_members' in obj:
            chat_members = obj['new_chat_members']
            nms = []
            for m in chat_members:
                nms.append(User.de_json(m))
            opts['new_chat_members'] = nms
            content_type = 'new_chat_members'
        if 'left_chat_member' in obj:
            opts['left_chat_member'] = User.de_json(obj['left_chat_member'])
            content_type = 'left_chat_member'
        if 'new_chat_title' in obj:
            opts['new_chat_title'] = obj['new_chat_title']
        if 'new_chat_photo' in obj:
            opts['new_chat_photo'] = Message.parse_photo(obj['new_chat_photo'])
        if 'delete_chat_photo' in obj:
            opts['delete_chat_photo'] = obj['delete_chat_photo']
        if 'group_chat_created' in obj:
            opts['group_chat_created'] = obj['group_chat_created']
        if 'supergroup_chat_created' in obj:
            opts['supergroup_chat_created'] = obj['supergroup_chat_created']
        if 'channel_chat_created' in obj:
            opts['channel_chat_created'] = obj['channel_chat_created']
        if 'migrate_to_chat_id' in obj:
            opts['migrate_to_chat_id'] = obj['migrate_to_chat_id']
        if 'migrate_from_chat_id' in obj:
            opts['migrate_from_chat_id'] = obj['migrate_from_chat_id']
        if 'pinned_message' in obj:
            opts['pinned_message'] = Message.de_json(obj['pinned_message'])
        if 'invoice' in obj:
            opts['invoice'] = Invoice.de_json(obj['invoice'])
            content_type = 'invoice'
        if 'successful_payment' in obj:
            opts['successful_payment'] = SuccessfulPayment.de_json(obj['successful_payment'])
            content_type = 'successful_payment'
        if 'video_chat_scheduled' in obj:
            opts['video_chat_scheduled'] = VideoChatScheduled.de_json(obj['video_chat_scheduled'])
            opts['voice_chat_scheduled'] = opts['video_chat_scheduled']  # deprecated, for backward compatibility
            content_type = 'video_chat_scheduled'
        if 'voice_chat_scheduled' in obj:
            opts['video_chat_scheduled'] = VideoChatScheduled.de_json(obj['voice_chat_scheduled'])
            opts['voice_chat_scheduled'] = opts['video_chat_scheduled']  # deprecated, for backward compatibility
            content_type = 'video_chat_scheduled'
        if 'video_chat_started' in obj:
            opts['video_chat_started'] = VideoChatStarted.de_json(obj['video_chat_started'])
            opts['voice_chat_started'] = opts['video_chat_started']  # deprecated, for backward compatibility
            content_type = 'video_chat_started'
        if 'video_chat_ended' in obj:
            opts['video_chat_ended'] = VideoChatEnded.de_json(obj['video_chat_ended'])
            opts['voice_chat_ended'] = opts['video_chat_ended']  # deprecated, for backward compatibility
            content_type = 'video_chat_ended'
        if 'video_chat_participants_invited' in obj:
            opts['video_chat_participants_invited'] = VideoChatParticipantsInvited.de_json(obj['video_chat_participants_invited'])
            opts['voice_chat_participants_invited'] = opts['video_chat_participants_invited']  # deprecated, for backward compatibility
            content_type = 'video_chat_participants_invited'
        if 'poll' in obj:
            opts['poll'] = Poll.de_json(obj['poll'])
            content_type = 'poll'
        if 'web_app_data' in obj:
            opts['web_app_data'] = WebAppData.de_json(obj['web_app_data'])
            content_type = 'web_app_data'
        return cls(message_id, from_user, date, chat, content_type, opts)

    @classmethod
    def parse_chat(cls, chat):
        if 'first_name' not in chat:
            return GroupChat.de_json(chat)
        else:
            return User.de_json(chat)

    @classmethod
    def parse_photo(cls, photo_size_array):
        ret = []
        for ps in photo_size_array:
            ret.append(PhotoSize.de_json(ps))
        return ret

    @classmethod
    def parse_entities(cls, message_entity_array):
        ret = []
        for me in message_entity_array:
            ret.append(MessageEntity.de_json(me))
        return ret

    def __init__(self, message_id, from_user, date, chat, content_type, options):
        self.content_type = content_type
        self.message_id = message_id
        self.from_user = from_user
        self.date = date
        self.chat = chat
        self.forward_from_chat = None
        self.forward_from = None
        self.forward_date = None
        self.reply_to_message = None
        self.edit_date = None
        self.author_signature = None
        self.text = None
        self.entities = None
        self.caption_entities = None
        self.audio = None
        self.document = None
        self.photo = None
        self.sticker = None
        self.video = None
        self.video_note = None
        self.voice = None
        self.caption = None
        self.contact = None
        self.location = None
        self.venue = None
        self.new_chat_member = None
        self.new_chat_members = None
        self.left_chat_member = None
        self.new_chat_title = None
        self.new_chat_photo = None
        self.delete_chat_photo = None
        self.group_chat_created = None
        self.supergroup_chat_created = None
        self.channel_chat_created = None
        self.migrate_to_chat_id = None
        self.migrate_from_chat_id = None
        self.pinned_message = None
        self.invoice = None
        self.successful_payment = None
        self.video_chat_scheduled = None
        self.video_chat_started = None
        self.video_chat_ended = None
        self.video_chat_participants_invited = None
        self.web_app_data = None
        for key in options:
            setattr(self, key, options[key])


class MessageEntity(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        type = obj['type']
        offset = obj['offset']
        length = obj['length']
        url = obj.get('url')
        user = None
        if 'user' in obj:
            user = User.de_json(obj['user'])
        return cls(type, offset, length, url, user)

    def __init__(self, type, offset, length, url=None, user=None):
        self.type = type
        self.offset = offset
        self.length = length
        self.url = url
        self.user = user


class PhotoSize(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        file_id = obj['file_id']
        width = obj['width']
        height = obj['height']
        file_size = obj.get('file_size')
        return cls(file_id, width, height, file_size)

    def __init__(self, file_id, width, height, file_size=None):
        self.file_size = file_size
        self.height = height
        self.width = width
        self.file_id = file_id


class Audio(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        file_id = obj['file_id']
        duration = obj['duration']
        performer = obj.get('performer')
        title = obj.get('title')
        mime_type = obj.get('mime_type')
        file_size = obj.get('file_size')
        return cls(file_id, duration, performer, title, mime_type, file_size)

    def __init__(self, file_id, duration, performer=None, title=None, mime_type=None, file_size=None):
        self.file_id = file_id
        self.duration = duration
        self.performer = performer
        self.title = title
        self.mime_type = mime_type
        self.file_size = file_size


class Voice(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        file_id = obj['file_id']
        duration = obj['duration']
        mime_type = obj.get('mime_type')
        file_size = obj.get('file_size')
        return cls(file_id, duration, mime_type, file_size)

    def __init__(self, file_id, duration, mime_type=None, file_size=None):
        self.file_id = file_id
        self.duration = duration
        self.mime_type = mime_type
        self.file_size = file_size


class Document(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        file_id = obj['file_id']
        thumb = None
        if 'thumb' in obj and 'file_id' in obj['thumb']:
            thumb = PhotoSize.de_json(obj['thumb'])
        file_name = obj.get('file_name')
        mime_type = obj.get('mime_type')
        file_size = obj.get('file_size')
        return cls(file_id, thumb, file_name, mime_type, file_size)

    def __init__(self, file_id, thumb=None, file_name=None, mime_type=None, file_size=None):
        self.file_id = file_id
        self.thumb = thumb
        self.file_name = file_name
        self.mime_type = mime_type
        self.file_size = file_size


class Sticker(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        file_id = obj['file_id']
        width = obj['width']
        height = obj['height']
        thumb = None
        if 'thumb' in obj:
            thumb = PhotoSize.de_json(obj['thumb'])
        emoji = obj.get('emoji')
        file_size = obj.get('file_size')
        return cls(file_id, width, height, thumb, emoji, file_size)

    def __init__(self, file_id, width, height, thumb, emoji=None, file_size=None):
        self.file_id = file_id
        self.width = width
        self.height = height
        self.thumb = thumb
        self.emoji = emoji
        self.file_size = file_size


class Video(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        file_id = obj['file_id']
        width = obj['width']
        height = obj['height']
        duration = obj['duration']
        thumb = None
        if 'thumb' in obj:
            thumb = PhotoSize.de_json(obj['thumb'])
        mime_type = obj.get('mime_type')
        file_size = obj.get('file_size')
        return cls(file_id, width, height, duration, thumb, mime_type, file_size)

    def __init__(self, file_id, width, height, duration, thumb=None, mime_type=None, file_size=None):
        self.file_id = file_id
        self.width = width
        self.height = height
        self.duration = duration
        self.thumb = thumb
        self.mime_type = mime_type
        self.file_size = file_size


class VideoNote(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        file_id = obj['file_id']
        length = obj['length']
        duration = obj['duration']
        thumb = None
        if 'thumb' in obj:
            thumb = PhotoSize.de_json(obj['thumb'])
        file_size = obj.get('file_size')
        return cls(file_id, length, duration, thumb, file_size)

    def __init__(self, file_id, length, duration, thumb=None, file_size=None):
        self.file_id = file_id
        self.length = length
        self.duration = duration
        self.thumb = thumb
        self.file_size = file_size


class Contact(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        phone_number = obj['phone_number']
        first_name = obj['first_name']
        last_name = obj.get('last_name')
        user_id = obj.get('user_id')
        return cls(phone_number, first_name, last_name, user_id)

    def __init__(self, phone_number, first_name, last_name=None, user_id=None):
        self.phone_number = phone_number
        self.first_name = first_name
        self.last_name = last_name
        self.user_id = user_id


class Location(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        longitude = obj['longitude']
        latitude = obj['latitude']
        return cls(longitude, latitude)

    def __init__(self, longitude, latitude):
        self.longitude = longitude
        self.latitude = latitude


class Venue(JsonDeserializable):
    @classmethod
    def de_json(cls, json_type):
        obj = cls.check_json(json_type)
        location = Location.de_json(obj['location'])
        title = obj['title']
        address = obj['address']
        foursquare_id = obj.get('foursquare_id')
        return cls(location, title, address, foursquare_id)

    def __init__(self, location, title, address, foursquare_id=None):
        self.location = location
        self.title = title
        self.address = address
        self.foursquare_id = foursquare_id


class UserProfilePhotos(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        total_count = obj['total_count']
        photos = [[PhotoSize.de_json(y) for y in x] for x in obj['photos']]
        return cls(total_count, photos)

    def __init__(self, total_count, photos):
        self.total_count = total_count
        self.photos = photos


class File(JsonDeserializable):
    @classmethod
    def de_json(cls, json_type):
        obj = cls.check_json(json_type)
        file_id = obj['file_id']
        file_size = obj.get('file_size')
        file_path = obj.get('file_path')
        return cls(file_id, file_size, file_path)

    def __init__(self, file_id, file_size, file_path):
        self.file_id = file_id
        self.file_size = file_size
        self.file_path = file_path


class ForceReply(JsonSerializable):
    def __init__(self, selective=None):
        self.selective = selective

    def to_json(self):
        json_dict = {'force_reply': True}
        if self.selective:
            json_dict['selective'] = True
        return json.dumps(json_dict)


class ReplyKeyboardRemove(JsonSerializable):
    def __init__(self, selective=None):
        self.selective = selective

    def to_json(self):
        json_dict = {'remove_keyboard': True}
        if self.selective:
            json_dict['selective'] = True
        return json.dumps(json_dict)


class ReplyKeyboardMarkup(JsonSerializable):
    def __init__(self, resize_keyboard=None, one_time_keyboard=None, selective=None, row_width=3):
        self.resize_keyboard = resize_keyboard
        self.one_time_keyboard = one_time_keyboard
        self.selective = selective
        self.row_width = row_width

        self.keyboard = []

    def add(self, *args):
        """
        This function adds strings to the keyboard, while not exceeding row_width.
        E.g. ReplyKeyboardMarkup#add("A", "B", "C") yields the json result {keyboard: [["A"], ["B"], ["C"]]}
        when row_width is set to 1.
        When row_width is set to 2, the following is the result of this function: {keyboard: [["A", "B"], ["C"]]}
        See https://core.telegram.org/bots/api#replykeyboardmarkup
        :param args: KeyboardButton to append to the keyboard
        """
        i = 1
        row = []
        for button in args:
            if util.is_string(button):
                row.append({'text': button})
            elif isinstance(button, bytes):
                row.append({'text': button.decode('utf-8')})
            else:
                row.append(button.to_dic())
            if i % self.row_width == 0:
                self.keyboard.append(row)
                row = []
            i += 1
        if len(row) > 0:
            self.keyboard.append(row)

    def row(self, *args):
        """
        Adds a list of KeyboardButton to the keyboard. This function does not consider row_width.
        ReplyKeyboardMarkup#row("A")#row("B", "C")#to_json() outputs '{keyboard: [["A"], ["B", "C"]]}'
        See https://core.telegram.org/bots/api#replykeyboardmarkup
        :param args: strings
        :return: self, to allow function chaining.
        """
        btn_array = []
        for button in args:
            if util.is_string(button):
                btn_array.append({'text': button})
            else:
                btn_array.append(button.to_dic())
        self.keyboard.append(btn_array)
        return self

    def to_json(self):
        """
        Converts this object to its json representation following the Telegram API guidelines described here:
        https://core.telegram.org/bots/api#replykeyboardmarkup
        :return:
        """
        json_dict = {'keyboard': self.keyboard}
        if self.one_time_keyboard:
            json_dict['one_time_keyboard'] = True

        if self.resize_keyboard:
            json_dict['resize_keyboard'] = True

        if self.selective:
            json_dict['selective'] = True

        return json.dumps(json_dict)


class WebAppInfo(JsonDeserializable, Dictionaryable):
    """
    Describes a Web App.

    Telegram Documentation: https://core.telegram.org/bots/api#webappinfo

    :param url: An HTTPS URL of a Web App to be opened with additional data as specified in Initializing Web Apps
    :type url: :obj:`str`

    :return: Instance of the class
    :rtype: :class:`telebot.types.WebAppInfo`
    """
    @classmethod
    def de_json(cls, json_string):
        if json_string is None: return None
        obj = cls.check_json(json_string)
        return cls(**obj)

    def __init__(self, url, **kwargs):
        self.url: str = url

    def to_dict(self):
        return {'url': self.url}


class KeyboardButtonPollType(Dictionaryable):
    """
    This object represents type of a poll, which is allowed to be created and sent when the corresponding button is pressed.

    Telegram Documentation: https://core.telegram.org/bots/api#keyboardbuttonpolltype

    :param type: Optional. If quiz is passed, the user will be allowed to create only polls in the quiz mode. If regular is
        passed, only regular polls will be allowed. Otherwise, the user will be allowed to create a poll of any type.
    :type type: :obj:`str`

    :return: Instance of the class
    :rtype: :class:`telebot.types.KeyboardButtonPollType`
    """
    def __init__(self, type=''):
        self.type: str = type

    def to_dict(self):
        return {'type': self.type}


class KeyboardButton(Dictionaryable, JsonSerializable):
    def __init__(self, text, request_contact=None, request_location=None,
                 request_poll: Optional[KeyboardButtonPollType]=None, web_app: Optional[WebAppInfo]=None):
        self.text = text
        self.request_contact = request_contact
        self.request_location = request_location
        self.request_poll: KeyboardButtonPollType = request_poll
        self.web_app: WebAppInfo = web_app

    def to_json(self):
        return json.dumps(self.to_dic())

    def to_dic(self):
        json_dic = {'text': self.text}
        if self.request_contact:
            json_dic['request_contact'] = self.request_contact
        if self.request_location:
            json_dic['request_location'] = self.request_location
        if self.request_poll is not None:
            json_dic['request_poll'] = self.request_poll.to_dict()
        if self.web_app is not None:
            json_dic['web_app'] = self.web_app.to_dict()
        return json_dic


class InlineKeyboardMarkup(Dictionaryable, JsonSerializable):
    def __init__(self, row_width=3):
        self.row_width = row_width

        self.keyboard = []

    def add(self, *args):
        """
        This function adds strings to the keyboard, while not exceeding row_width.
        E.g. ReplyKeyboardMarkup#add("A", "B", "C") yields the json result {keyboard: [["A"], ["B"], ["C"]]}
        when row_width is set to 1.
        When row_width is set to 2, the following is the result of this function: {keyboard: [["A", "B"], ["C"]]}
        See https://core.telegram.org/bots/api#replykeyboardmarkup
        :param args: KeyboardButton to append to the keyboard
        """
        i = 1
        row = []
        for button in args:
            row.append(button.to_dic())
            if i % self.row_width == 0:
                self.keyboard.append(row)
                row = []
            i += 1
        if len(row) > 0:
            self.keyboard.append(row)

    def row(self, *args):
        """
        Adds a list of KeyboardButton to the keyboard. This function does not consider row_width.
        ReplyKeyboardMarkup#row("A")#row("B", "C")#to_json() outputs '{keyboard: [["A"], ["B", "C"]]}'
        See https://core.telegram.org/bots/api#inlinekeyboardmarkup
        :param args: strings
        :return: self, to allow function chaining.
        """
        btn_array = []
        for button in args:
            btn_array.append(button.to_dic())
        self.keyboard.append(btn_array)
        return self

    def to_json(self):
        """
        Converts this object to its json representation following the Telegram API guidelines described here:
        https://core.telegram.org/bots/api#inlinekeyboardmarkup
        :return:
        """
        json_dict = {'inline_keyboard': self.keyboard}
        return json.dumps(json_dict)

    def to_dic(self):
        json_dict = {'inline_keyboard': self.keyboard}
        return json_dict


class SwitchInlineQueryChosenChat(JsonDeserializable, Dictionaryable, JsonSerializable):
    """
    Represents an inline button that switches the current user to inline mode in a chosen chat,
    with an optional default inline query.

    Telegram Documentation: https://core.telegram.org/bots/api#inlinekeyboardbutton

    :param query: Optional. The default inline query to be inserted in the input field.
                  If left empty, only the bot's username will be inserted
    :type query: :obj:`str`

    :param allow_user_chats: Optional. True, if private chats with users can be chosen
    :type allow_user_chats: :obj:`bool`

    :param allow_bot_chats: Optional. True, if private chats with bots can be chosen
    :type allow_bot_chats: :obj:`bool`

    :param allow_group_chats: Optional. True, if group and supergroup chats can be chosen
    :type allow_group_chats: :obj:`bool`

    :param allow_channel_chats: Optional. True, if channel chats can be chosen
    :type allow_channel_chats: :obj:`bool`

    :return: Instance of the class
    :rtype: :class:`SwitchInlineQueryChosenChat`
    """

    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None
        obj = cls.check_json(json_string)
        return cls(**obj)

    def __init__(self, query=None, allow_user_chats=None, allow_bot_chats=None, allow_group_chats=None,
                 allow_channel_chats=None):
        self.query: str = query
        self.allow_user_chats: bool = allow_user_chats
        self.allow_bot_chats: bool = allow_bot_chats
        self.allow_group_chats: bool = allow_group_chats
        self.allow_channel_chats: bool = allow_channel_chats

    def to_dict(self):
        json_dict = {}

        if self.query is not None:
            json_dict['query'] = self.query
        if self.allow_user_chats is not None:
            json_dict['allow_user_chats'] = self.allow_user_chats
        if self.allow_bot_chats is not None:
            json_dict['allow_bot_chats'] = self.allow_bot_chats
        if self.allow_group_chats is not None:
            json_dict['allow_group_chats'] = self.allow_group_chats
        if self.allow_channel_chats is not None:
            json_dict['allow_channel_chats'] = self.allow_channel_chats

        return json_dict

    def to_json(self):
        return json.dumps(self.to_dict())


class SentWebAppMessage(JsonDeserializable, Dictionaryable):
    """
    Describes an inline message sent by a Web App on behalf of a user.

    Telegram Documentation: https://core.telegram.org/bots/api#sentwebappmessage

    :param inline_message_id: Optional. Identifier of the sent inline message. Available only if there is an inline
        keyboard attached to the message.
    :type inline_message_id: :obj:`str`

    :return: Instance of the class
    :rtype: :class:`telebot.types.SentWebAppMessage`
    """
    @classmethod
    def de_json(cls, json_string):
        if json_string is None: return None
        obj = cls.check_json(json_string)
        return cls(**obj)

    def __init__(self, inline_message_id=None):
        self.inline_message_id = inline_message_id

    def to_dict(self):
        json_dict = {}
        if self.inline_message_id:
            json_dict['inline_message_id'] = self.inline_message_id
        return json_dict


class InlineKeyboardButton(Dictionaryable, JsonSerializable, JsonDeserializable):
    def __init__(self, text, url=None, callback_data=None, web_app=None, switch_inline_query=None,
                 switch_inline_query_current_chat=None, callback_game=None, pay=None):
        self.text = text
        self.url = url
        self.callback_data = callback_data
        self.web_app: WebAppInfo = web_app
        self.switch_inline_query = switch_inline_query
        self.switch_inline_query_current_chat = switch_inline_query_current_chat
        self.callback_game = callback_game
        self.pay = pay

    @classmethod
    def de_json(cls, json_string):
        if json_string is None: return None
        obj = cls.check_json(json_string)
        if 'web_app' in obj:
            obj['web_app'] = WebAppInfo.de_json(obj.get('web_app'))
        if 'switch_inline_query_chosen_chat' in obj:
            obj['switch_inline_query_chosen_chat'] = SwitchInlineQueryChosenChat.de_json(
                obj.get('switch_inline_query_chosen_chat')
            )

        return cls(**obj)

    def to_json(self):
        return json.dumps(self.to_dic())

    def to_dic(self):
        json_dic = {'text': self.text}
        if self.url:
            json_dic['url'] = self.url
        if self.callback_data:
            json_dic['callback_data'] = self.callback_data
        if self.web_app:
            json_dic['web_app'] = self.web_app.to_dict()
        if self.switch_inline_query is not None:
            json_dic['switch_inline_query'] = self.switch_inline_query
        if self.switch_inline_query_current_chat is not None:
            json_dic['switch_inline_query_current_chat'] = self.switch_inline_query_current_chat
        if self.callback_game is not None:
            json_dic['callback_game'] = self.callback_game
        if self.pay is not None:
            json_dic['pay'] = self.pay
        return json_dic


class CallbackQuery(JsonDeserializable):
    @classmethod
    def de_json(cls, json_type):
        obj = cls.check_json(json_type)
        id = obj['id']
        from_user = User.de_json(obj['from'])
        message = None
        if 'message' in obj:
            message = Message.de_json(obj['message'])
        inline_message_id = obj.get('inline_message_id')
        chat_instance = obj['chat_instance']
        data = obj.get('data')
        game_short_name = obj.get('game_short_name')
        return cls(id, from_user, data, chat_instance, message, inline_message_id, game_short_name)

    def __init__(self, id, from_user, data, chat_instance, message=None, inline_message_id=None, game_short_name=None):
        self.game_short_name = game_short_name
        self.chat_instance = chat_instance
        self.id = id
        self.from_user = from_user
        self.message = message
        self.data = data
        self.inline_message_id = inline_message_id


class ChatPhoto(JsonDeserializable):
    @classmethod
    def de_json(cls, json_type):
        obj = cls.check_json(json_type)
        small_file_id = obj['small_file_id']
        big_file_id = obj['big_file_id']
        return cls(small_file_id, big_file_id)

    def __init__(self, small_file_id, big_file_id):
        self.small_file_id = small_file_id
        self.big_file_id = big_file_id


class ChatMember(JsonDeserializable):
    @classmethod
    def de_json(cls, json_type):
        obj = cls.check_json(json_type)
        user = User.de_json(obj['user'])
        status = obj['status']
        until_date = obj.get('until_date')
        can_be_edited = obj.get('can_be_edited')
        can_change_info = obj.get('can_change_info')
        can_post_messages = obj.get('can_post_messages')
        can_edit_messages = obj.get('can_edit_messages')
        can_delete_messages = obj.get('can_delete_messages')
        can_invite_users = obj.get('can_invite_users')
        can_restrict_members = obj.get('can_restrict_members')
        can_pin_messages = obj.get('can_pin_messages')
        can_promote_members = obj.get('can_promote_members')
        can_send_messages = obj.get('can_send_messages')
        can_send_media_messages = obj.get('can_send_media_messages')
        can_send_other_messages = obj.get('can_send_other_messages')
        can_add_web_page_previews = obj.get('can_add_web_page_previews')
        can_manage_video_chats = obj.get('can_manage_video_chats')
        return cls(user, status, until_date, can_be_edited, can_change_info, can_post_messages, can_edit_messages,
                   can_delete_messages, can_invite_users, can_restrict_members, can_pin_messages, can_promote_members,
                   can_send_messages, can_send_media_messages, can_send_other_messages, can_add_web_page_previews,
                   can_manage_video_chats=can_manage_video_chats)

    def __init__(self, user, status, until_date, can_be_edited, can_change_info, can_post_messages, can_edit_messages,
                 can_delete_messages, can_invite_users, can_restrict_members, can_pin_messages, can_promote_members,
                 can_send_messages, can_send_media_messages, can_send_other_messages, can_add_web_page_previews,
                 can_manage_video_chats=None):
        self.user = user
        self.status = status
        self.until_date = until_date
        self.can_be_edited = can_be_edited
        self.can_change_info = can_change_info
        self.can_post_messages = can_post_messages
        self.can_edit_messages = can_edit_messages
        self.can_delete_messages = can_delete_messages
        self.can_invite_users = can_invite_users
        self.can_restrict_members = can_restrict_members
        self.can_pin_messages = can_pin_messages
        self.can_promote_members = can_promote_members
        self.can_send_messages = can_send_messages
        self.can_send_media_messages = can_send_media_messages
        self.can_send_other_messages = can_send_other_messages
        self.can_add_web_page_previews = can_add_web_page_previews
        self.can_manage_video_chats = can_manage_video_chats


# InlineQuery

class InlineQuery(JsonDeserializable):
    @classmethod
    def de_json(cls, json_type):
        obj = cls.check_json(json_type)
        id = obj['id']
        from_user = User.de_json(obj['from'])
        location = None
        if 'location' in obj:
            location = Location.de_json(obj['location'])
        query = obj['query']
        offset = obj['offset']
        return cls(id, from_user, location, query, offset)

    def __init__(self, id, from_user, location, query, offset):
        """
        This object represents an incoming inline query.
        When the user sends an empty query, your bot could
        return some default or trending results.
        :param id: string Unique identifier for this query
        :param from_user: User Sender
        :param location: Sender location, only for bots that request user location
        :param query: String Text of the query
        :param offset: String Offset of the results to be returned, can be controlled by the bot
        :return: InlineQuery Object
        """
        self.id = id
        self.from_user = from_user
        self.location = location
        self.query = query
        self.offset = offset


class InputTextMessageContent(Dictionaryable):
    def __init__(self, message_text, parse_mode=None, disable_web_page_preview=None):
        self.message_text = message_text
        self.parse_mode = parse_mode
        self.disable_web_page_preview = disable_web_page_preview

    def to_dic(self):
        json_dic = {'message_text': self.message_text}
        if self.parse_mode:
            json_dic['parse_mode'] = self.parse_mode
        if self.disable_web_page_preview:
            json_dic['disable_web_page_preview'] = self.disable_web_page_preview
        return json_dic


class InputLocationMessageContent(Dictionaryable):
    def __init__(self, latitude, longitude, live_period=None):
        self.latitude = latitude
        self.longitude = longitude
        self.live_period = live_period

    def to_dic(self):
        json_dic = {'latitude': self.latitude, 'longitude': self.longitude}
        if self.live_period:
            json_dic['live_period'] = self.live_period
        return json_dic


class InputVenueMessageContent(Dictionaryable):
    def __init__(self, latitude, longitude, title, address, foursquare_id=None):
        self.latitude = latitude
        self.longitude = longitude
        self.title = title
        self.address = address
        self.foursquare_id = foursquare_id

    def to_dic(self):
        json_dic = {'latitude': self.latitude, 'longitude': self.longitude, 'title': self.title,
                    'address': self.address}
        if self.foursquare_id:
            json_dic['foursquare_id'] = self.foursquare_id
        return json_dic


class InputContactMessageContent(Dictionaryable):
    def __init__(self, phone_number, first_name, last_name=None):
        self.phone_number = phone_number
        self.first_name = first_name
        self.last_name = last_name

    def to_dic(self):
        json_dic = {'phone_numbe': self.phone_number, 'first_name': self.first_name}
        if self.last_name:
            json_dic['last_name'] = self.last_name
        return json_dic


class ChosenInlineResult(JsonDeserializable):
    @classmethod
    def de_json(cls, json_type):
        obj = cls.check_json(json_type)
        result_id = obj['result_id']
        from_user = User.de_json(obj['from'])
        query = obj['query']
        location = None
        if 'location' in obj:
            location = Location.de_json(obj['location'])
        inline_message_id = obj.get('inline_message_id')
        return cls(result_id, from_user, query, location, inline_message_id)

    def __init__(self, result_id, from_user, query, location=None, inline_message_id=None):
        """
        This object represents a result of an inline query
        that was chosen by the user and sent to their chat partner.
        :param result_id: string The unique identifier for the result that was chosen.
        :param from_user: User The user that chose the result.
        :param query: String The query that was used to obtain the result.
        :return: ChosenInlineResult Object.
        """
        self.result_id = result_id
        self.from_user = from_user
        self.query = query
        self.location = location
        self.inline_message_id = inline_message_id


class InlineQueryResultArticle(JsonSerializable):
    def __init__(self, id, title, input_message_content, reply_markup=None, url=None,
                 hide_url=None, description=None, thumb_url=None, thumb_width=None, thumb_height=None):
        """
        Represents a link to an article or web page.
        :param id: Unique identifier for this result, 1-64 Bytes.
        :param title: Title of the result.
        :param input_message_content: InputMessageContent : Content of the message to be sent
        :param reply_markup: InlineKeyboardMarkup : Inline keyboard attached to the message
        :param url: URL of the result.
        :param hide_url: Pass True, if you don't want the URL to be shown in the message.
        :param description: Short description of the result.
        :param thumb_url: Url of the thumbnail for the result.
        :param thumb_width: Thumbnail width.
        :param thumb_height: Thumbnail height
        :return:
        """
        self.type = 'article'
        self.id = id
        self.title = title
        self.input_message_content = input_message_content
        self.reply_markup = reply_markup
        self.url = url
        self.hide_url = hide_url
        self.description = description
        self.thumb_url = thumb_url
        self.thumb_width = thumb_width
        self.thumb_height = thumb_height

    def to_json(self):
        json_dict = {'type': self.type, 'id': self.id, 'title': self.title,
                     'input_message_content': self.input_message_content.to_dic()}
        if self.reply_markup:
            json_dict['reply_markup'] = self.reply_markup.to_dic()
        if self.url:
            json_dict['url'] = self.url
        if self.hide_url:
            json_dict['hide_url'] = self.hide_url
        if self.description:
            json_dict['description'] = self.description
        if self.thumb_url:
            json_dict['thumb_url'] = self.thumb_url
        if self.thumb_width:
            json_dict['thumb_width'] = self.thumb_width
        if self.thumb_height:
            json_dict['thumb_height'] = self.thumb_height
        return json.dumps(json_dict)


class InlineQueryResultPhoto(JsonSerializable):
    def __init__(self, id, photo_url, thumb_url, photo_width=None, photo_height=None, title=None,
                 description=None, caption=None, reply_markup=None, input_message_content=None):
        """
        Represents a link to a photo.
        :param id: Unique identifier for this result, 1-64 bytes
        :param photo_url: A valid URL of the photo. Photo must be in jpeg format. Photo size must not exceed 5MB
        :param thumb_url: URL of the thumbnail for the photo
        :param photo_width: Width of the photo.
        :param photo_height: Height of the photo.
        :param title: Title for the result.
        :param description: Short description of the result.
        :param caption: Caption of the photo to be sent, 0-200 characters.
        :param reply_markup: InlineKeyboardMarkup : Inline keyboard attached to the message
        :param input_message_content: InputMessageContent : Content of the message to be sent instead of the photo
        :return:
        """
        self.type = 'photo'
        self.id = id
        self.photo_url = photo_url
        self.photo_width = photo_width
        self.photo_height = photo_height
        self.thumb_url = thumb_url
        self.title = title
        self.description = description
        self.caption = caption
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content

    def to_json(self):
        json_dict = {'type': self.type, 'id': self.id, 'photo_url': self.photo_url, 'thumb_url': self.thumb_url}
        if self.photo_width:
            json_dict['photo_width'] = self.photo_width
        if self.photo_height:
            json_dict['photo_height'] = self.photo_height
        if self.title:
            json_dict['title'] = self.title
        if self.description:
            json_dict['description'] = self.description
        if self.caption:
            json_dict['caption'] = self.caption
        if self.reply_markup:
            json_dict['reply_markup'] = self.reply_markup.to_dic()
        if self.input_message_content:
            json_dict['input_message_content'] = self.input_message_content.to_dic()
        return json.dumps(json_dict)


class InlineQueryResultGif(JsonSerializable):
    def __init__(self, id, gif_url, thumb_url, gif_width=None, gif_height=None, title=None, caption=None,
                 reply_markup=None, input_message_content=None, gif_duration=None):
        """
        Represents a link to an animated GIF file.
        :param id: Unique identifier for this result, 1-64 bytes.
        :param gif_url: A valid URL for the GIF file. File size must not exceed 1MB
        :param thumb_url: URL of the static thumbnail (jpeg or gif) for the result.
        :param gif_width: Width of the GIF.
        :param gif_height: Height of the GIF.
        :param title: Title for the result.
        :param caption:  Caption of the GIF file to be sent, 0-200 characters
        :param reply_markup: InlineKeyboardMarkup : Inline keyboard attached to the message
        :param input_message_content: InputMessageContent : Content of the message to be sent instead of the photo
        :return:
        """
        self.type = 'gif'
        self.id = id
        self.gif_url = gif_url
        self.gif_width = gif_width
        self.gif_height = gif_height
        self.thumb_url = thumb_url
        self.title = title
        self.caption = caption
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content
        self.gif_duration = gif_duration

    def to_json(self):
        json_dict = {'type': self.type, 'id': self.id, 'gif_url': self.gif_url, 'thumb_url': self.thumb_url}
        if self.gif_height:
            json_dict['gif_height'] = self.gif_height
        if self.gif_width:
            json_dict['gif_width'] = self.gif_width
        if self.title:
            json_dict['title'] = self.title
        if self.caption:
            json_dict['caption'] = self.caption
        if self.reply_markup:
            json_dict['reply_markup'] = self.reply_markup.to_dic()
        if self.input_message_content:
            json_dict['input_message_content'] = self.input_message_content.to_dic()
        if self.gif_duration:
            json_dict['gif_duration'] = self.gif_duration
        return json.dumps(json_dict)


class InlineQueryResultMpeg4Gif(JsonSerializable):
    def __init__(self, id, mpeg4_url, thumb_url, mpeg4_width=None, mpeg4_height=None, title=None, caption=None,
                 reply_markup=None, input_message_content=None, mpeg4_duration=None):
        """
        Represents a link to a video animation (H.264/MPEG-4 AVC video without sound).
        :param id: Unique identifier for this result, 1-64 bytes
        :param mpeg4_url: A valid URL for the MP4 file. File size must not exceed 1MB
        :param thumb_url: URL of the static thumbnail (jpeg or gif) for the result
        :param mpeg4_width: Video width
        :param mpeg4_height: Video height
        :param title: Title for the result
        :param caption: Caption of the MPEG-4 file to be sent, 0-200 characters
        :param reply_markup: InlineKeyboardMarkup : Inline keyboard attached to the message
        :param input_message_content: InputMessageContent : Content of the message to be sent instead of the photo
        :return:
        """
        self.type = 'mpeg4_gif'
        self.id = id
        self.mpeg4_url = mpeg4_url
        self.mpeg4_width = mpeg4_width
        self.mpeg4_height = mpeg4_height
        self.thumb_url = thumb_url
        self.title = title
        self.caption = caption
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content
        self.mpeg4_duration = mpeg4_duration

    def to_json(self):
        json_dict = {'type': self.type, 'id': self.id, 'mpeg4_url': self.mpeg4_url, 'thumb_url': self.thumb_url}
        if self.mpeg4_width:
            json_dict['mpeg4_width'] = self.mpeg4_width
        if self.mpeg4_height:
            json_dict['mpeg4_height'] = self.mpeg4_height
        if self.title:
            json_dict['title'] = self.title
        if self.caption:
            json_dict['caption'] = self.caption
        if self.reply_markup:
            json_dict['reply_markup'] = self.reply_markup.to_dic()
        if self.input_message_content:
            json_dict['input_message_content'] = self.input_message_content.to_dic()
        if self.mpeg4_duration:
            json_dict['mpeg4_duration '] = self.mpeg4_duration
        return json.dumps(json_dict)


class InlineQueryResultVideo(JsonSerializable):
    def __init__(self, id, video_url, mime_type, thumb_url, title,
                 caption=None, video_width=None, video_height=None, video_duration=None, description=None,
                 reply_markup=None, input_message_content=None):
        """
        Represents link to a page containing an embedded video player or a video file.
        :param id: Unique identifier for this result, 1-64 bytes
        :param video_url: A valid URL for the embedded video player or video file
        :param mime_type: Mime type of the content of video url, “text/html” or “video/mp4”
        :param thumb_url: URL of the thumbnail (jpeg only) for the video
        :param title: Title for the result
        :param video_width: Video width
        :param video_height: Video height
        :param video_duration: Video duration in seconds
        :param description: Short description of the result
        :return:
        """
        self.type = 'video'
        self.id = id
        self.video_url = video_url
        self.mime_type = mime_type
        self.video_width = video_width
        self.video_height = video_height
        self.video_duration = video_duration
        self.thumb_url = thumb_url
        self.title = title
        self.caption = caption
        self.description = description
        self.input_message_content = input_message_content
        self.reply_markup = reply_markup

    def to_json(self):
        json_dict = {'type': self.type, 'id': self.id, 'video_url': self.video_url, 'mime_type': self.mime_type,
                     'thumb_url': self.thumb_url, 'title': self.title}
        if self.video_width:
            json_dict['video_width'] = self.video_width
        if self.video_height:
            json_dict['video_height'] = self.video_height
        if self.video_duration:
            json_dict['video_duration'] = self.video_duration
        if self.description:
            json_dict['description'] = self.description
        if self.caption:
            json_dict['caption'] = self.caption
        if self.reply_markup:
            json_dict['reply_markup'] = self.reply_markup.to_dic()
        if self.input_message_content:
            json_dict['input_message_content'] = self.input_message_content.to_dic()
        return json.dumps(json_dict)


class InlineQueryResultAudio(JsonSerializable):
    def __init__(self, id, audio_url, title, caption=None, performer=None, audio_duration=None, reply_markup=None,
                 input_message_content=None):
        self.type = 'audio'
        self.id = id
        self.audio_url = audio_url
        self.title = title
        self.caption = caption
        self.performer = performer
        self.audio_duration = audio_duration
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content

    def to_json(self):
        json_dict = {'type': self.type, 'id': self.id, 'audio_url': self.audio_url, 'title': self.title}
        if self.caption:
            json_dict['caption'] = self.caption
        if self.performer:
            json_dict['performer'] = self.performer
        if self.audio_duration:
            json_dict['audio_duration'] = self.audio_duration
        if self.reply_markup:
            json_dict['reply_markup'] = self.reply_markup.to_dic()
        if self.input_message_content:
            json_dict['input_message_content'] = self.input_message_content.to_dic()
        return json.dumps(json_dict)


class InlineQueryResultVoice(JsonSerializable):
    def __init__(self, id, voice_url, title, caption=None, performer=None, voice_duration=None, reply_markup=None,
                 input_message_content=None):
        self.type = 'voice'
        self.id = id
        self.voice_url = voice_url
        self.title = title
        self.caption = caption
        self.performer = performer
        self.voice_duration = voice_duration
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content

    def to_json(self):
        json_dict = {'type': self.type, 'id': self.id, 'voice_url': self.voice_url, 'title': self.title}
        if self.caption:
            json_dict['caption'] = self.caption
        if self.performer:
            json_dict['performer'] = self.performer
        if self.voice_duration:
            json_dict['voice_duration'] = self.voice_duration
        if self.reply_markup:
            json_dict['reply_markup'] = self.reply_markup.to_dic()
        if self.input_message_content:
            json_dict['input_message_content'] = self.input_message_content.to_dic()
        return json.dumps(json_dict)


class InlineQueryResultDocument(JsonSerializable):
    def __init__(self, id, title, document_url, mime_type, caption=None, description=None, reply_markup=None,
                 input_message_content=None, thumb_url=None, thumb_width=None, thumb_height=None):
        self.type = 'document'
        self.id = id
        self.title = title
        self.document_url = document_url
        self.mime_type = mime_type
        self.caption = caption
        self.description = description
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content
        self.thumb_url = thumb_url
        self.thumb_width = thumb_width
        self.thumb_height = thumb_height

    def to_json(self):
        json_dict = {'type': self.type, 'id': self.id, 'title': self.title, 'document_url': self.document_url,
                     'mime_type': self.mime_type}
        if self.caption:
            json_dict['caption'] = self.caption
        if self.description:
            json_dict['description'] = self.description
        if self.thumb_url:
            json_dict['thumb_url'] = self.thumb_url
        if self.thumb_width:
            json_dict['thumb_width'] = self.thumb_width
        if self.thumb_height:
            json_dict['thumb_height'] = self.thumb_height
        if self.reply_markup:
            json_dict['reply_markup'] = self.reply_markup.to_dic()
        if self.input_message_content:
            json_dict['input_message_content'] = self.input_message_content.to_dic()
        return json.dumps(json_dict)


class InlineQueryResultLocation(JsonSerializable):
    def __init__(self, id, title, latitude, longitude, live_period=None, reply_markup=None,
                 input_message_content=None, thumb_url=None, thumb_width=None, thumb_height=None):
        self.type = 'location'
        self.id = id
        self.title = title
        self.latitude = latitude
        self.longitude = longitude
        self.live_period = live_period
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content
        self.thumb_url = thumb_url
        self.thumb_width = thumb_width
        self.thumb_height = thumb_height

    def to_json(self):
        json_dict = {'type': self.type, 'id': self.id, 'latitude': self.latitude, 'longitude': self.longitude,
                     'title': self.title}
        if self.live_period:
            json_dict['live_period'] = self.live_period
        if self.thumb_url:
            json_dict['thumb_url'] = self.thumb_url
        if self.thumb_width:
            json_dict['thumb_width'] = self.thumb_width
        if self.thumb_height:
            json_dict['thumb_height'] = self.thumb_height
        if self.reply_markup:
            json_dict['reply_markup'] = self.reply_markup.to_dic()
        if self.input_message_content:
            json_dict['input_message_content'] = self.input_message_content.to_dic()
        return json.dumps(json_dict)


class InlineQueryResultVenue(JsonSerializable):
    def __init__(self, id, title, latitude, longitude, address, foursquare_id=None, reply_markup=None,
                 input_message_content=None, thumb_url=None, thumb_width=None, thumb_height=None):
        self.type = 'venue'
        self.id = id
        self.title = title
        self.latitude = latitude
        self.longitude = longitude
        self.address = address
        self.foursquare_id = foursquare_id
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content
        self.thumb_url = thumb_url
        self.thumb_width = thumb_width
        self.thumb_height = thumb_height

    def to_json(self):
        json_dict = {'type': self.type, 'id': self.id, 'title': self.title, 'latitude': self.latitude,
                     'longitude': self.longitude, 'address': self.address}
        if self.foursquare_id:
            json_dict['foursquare_id'] = self.foursquare_id
        if self.thumb_url:
            json_dict['thumb_url'] = self.thumb_url
        if self.thumb_width:
            json_dict['thumb_width'] = self.thumb_width
        if self.thumb_height:
            json_dict['thumb_height'] = self.thumb_height
        if self.reply_markup:
            json_dict['reply_markup'] = self.reply_markup.to_dic()
        if self.input_message_content:
            json_dict['input_message_content'] = self.input_message_content.to_dic()
        return json.dumps(json_dict)


class InlineQueryResultContact(JsonSerializable):
    def __init__(self, id, phone_number, first_name, last_name=None, reply_markup=None,
                 input_message_content=None, thumb_url=None, thumb_width=None, thumb_height=None):
        self.type = 'contact'
        self.id = id
        self.phone_number = phone_number
        self.first_name = first_name
        self.last_name = last_name
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content
        self.thumb_url = thumb_url
        self.thumb_width = thumb_width
        self.thumb_height = thumb_height

    def to_json(self):
        json_dict = {'type': self.type, 'id': self.id, 'phone_number': self.phone_number, 'first_name': self.first_name}
        if self.last_name:
            json_dict['last_name'] = self.last_name
        if self.thumb_url:
            json_dict['thumb_url'] = self.thumb_url
        if self.thumb_width:
            json_dict['thumb_width'] = self.thumb_width
        if self.thumb_height:
            json_dict['thumb_height'] = self.thumb_height
        if self.reply_markup:
            json_dict['reply_markup'] = self.reply_markup.to_dic()
        if self.input_message_content:
            json_dict['input_message_content'] = self.input_message_content.to_dic()
        return json.dumps(json_dict)


class BaseInlineQueryResultCached(JsonSerializable):
    def __init__(self):
        self.type = None
        self.id = None
        self.title = None
        self.description = None
        self.caption = None
        self.reply_markup = None
        self.input_message_content = None
        self.payload_dic = {}

    def to_json(self):
        json_dict = self.payload_dic
        json_dict['type'] = self.type
        json_dict['id'] = self.id
        if self.title:
            json_dict['title'] = self.title
        if self.description:
            json_dict['description'] = self.description
        if self.caption:
            json_dict['caption'] = self.caption
        if self.reply_markup:
            json_dict['reply_markup'] = self.reply_markup.to_dic()
        if self.input_message_content:
            json_dict['input_message_content'] = self.input_message_content.to_dic()
        return json.dumps(json_dict)


class InlineQueryResultBase(BaseInlineQueryResultCached, Dictionaryable, JsonSerializable):
    """
    This object represents one result of an inline query. Telegram clients currently support results of the following 20 types:

    * :class:`InlineQueryResultCachedAudio`
    * :class:`InlineQueryResultCachedDocument`
    * :class:`InlineQueryResultCachedGif`
    * :class:`InlineQueryResultCachedMpeg4Gif`
    * :class:`InlineQueryResultCachedPhoto`
    * :class:`InlineQueryResultCachedSticker`
    * :class:`InlineQueryResultCachedVideo`
    * :class:`InlineQueryResultCachedVoice`
    * :class:`InlineQueryResultArticle`
    * :class:`InlineQueryResultAudio`
    * :class:`InlineQueryResultContact`
    * :class:`InlineQueryResultGame`
    * :class:`InlineQueryResultDocument`
    * :class:`InlineQueryResultGif`
    * :class:`InlineQueryResultLocation`
    * :class:`InlineQueryResultMpeg4Gif`
    * :class:`InlineQueryResultPhoto`
    * :class:`InlineQueryResultVenue`
    * :class:`InlineQueryResultVideo`
    * :class:`InlineQueryResultVoice`

    Telegram Documentation: https://core.telegram.org/bots/api#inlinequeryresult
    """
    # noinspection PyShadowingBuiltins
    def __init__(self, type, id, title = None, caption = None, input_message_content = None,
                 reply_markup = None, caption_entities = None, parse_mode = None):
        super().__init__()
        self.type = type
        self.id = id
        self.title = title
        self.caption = caption
        self.input_message_content = input_message_content
        self.reply_markup = reply_markup
        self.caption_entities = caption_entities
        self.parse_mode = parse_mode

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        json_dict = {
            'type': self.type,
            'id': self.id
        }
        if self.title:
            json_dict['title'] = self.title
        if self.caption:
            json_dict['caption'] = self.caption
        if self.input_message_content:
            json_dict['input_message_content'] = self.input_message_content.to_dict()
        if self.reply_markup:
            json_dict['reply_markup'] = self.reply_markup.to_dict()
        if self.caption_entities:
            json_dict['caption_entities'] = MessageEntity.to_list_of_dicts(self.caption_entities)
        if self.parse_mode:
            json_dict['parse_mode'] = self.parse_mode
        return json_dict



class InlineQueryResultCachedPhoto(BaseInlineQueryResultCached):
    def __init__(self, id, photo_file_id, title=None, description=None, caption=None, reply_markup=None,
                 input_message_content=None):
        BaseInlineQueryResultCached.__init__(self)
        self.type = 'photo'
        self.id = id
        self.photo_file_id = photo_file_id
        self.title = title
        self.description = description
        self.caption = caption
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content
        self.payload_dic['photo_file_id'] = photo_file_id


class InlineQueryResultCachedGif(BaseInlineQueryResultCached):
    def __init__(self, id, gif_file_id, title=None, description=None, caption=None, reply_markup=None,
                 input_message_content=None):
        BaseInlineQueryResultCached.__init__(self)
        self.type = 'gif'
        self.id = id
        self.gif_file_id = gif_file_id
        self.title = title
        self.description = description
        self.caption = caption
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content
        self.payload_dic['gif_file_id'] = gif_file_id


class InlineQueryResultCachedMpeg4Gif(BaseInlineQueryResultCached):
    def __init__(self, id, mpeg4_file_id, title=None, description=None, caption=None, reply_markup=None,
                 input_message_content=None):
        BaseInlineQueryResultCached.__init__(self)
        self.type = 'mpeg4_gif'
        self.id = id
        self.mpeg4_file_id = mpeg4_file_id
        self.title = title
        self.description = description
        self.caption = caption
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content
        self.payload_dic['mpeg4_file_id'] = mpeg4_file_id


class InlineQueryResultCachedSticker(BaseInlineQueryResultCached):
    def __init__(self, id, sticker_file_id, reply_markup=None, input_message_content=None):
        BaseInlineQueryResultCached.__init__(self)
        self.type = 'sticker'
        self.id = id
        self.sticker_file_id = sticker_file_id
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content
        self.payload_dic['sticker_file_id'] = sticker_file_id


class InlineQueryResultCachedDocument(BaseInlineQueryResultCached):
    def __init__(self, id, document_file_id, title, description=None, caption=None, reply_markup=None,
                 input_message_content=None):
        BaseInlineQueryResultCached.__init__(self)
        self.type = 'document'
        self.id = id
        self.document_file_id = document_file_id
        self.title = title
        self.description = description
        self.caption = caption
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content
        self.payload_dic['document_file_id'] = document_file_id


class InlineQueryResultCachedVideo(BaseInlineQueryResultCached):
    def __init__(self, id, video_file_id, title, description=None, caption=None, reply_markup=None,
                 input_message_content=None):
        BaseInlineQueryResultCached.__init__(self)
        self.type = 'video'
        self.id = id
        self.video_file_id = video_file_id
        self.title = title
        self.description = description
        self.caption = caption
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content
        self.payload_dic['video_file_id'] = video_file_id


class InlineQueryResultCachedVoice(BaseInlineQueryResultCached):
    def __init__(self, id, voice_file_id, title, caption=None, reply_markup=None, input_message_content=None):
        BaseInlineQueryResultCached.__init__(self)
        self.type = 'voice'
        self.id = id
        self.voice_file_id = voice_file_id
        self.title = title
        self.caption = caption
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content
        self.payload_dic['voice_file_id'] = voice_file_id


class InlineQueryResultCachedAudio(BaseInlineQueryResultCached):
    def __init__(self, id, audio_file_id, caption=None, reply_markup=None, input_message_content=None):
        BaseInlineQueryResultCached.__init__(self)
        self.type = 'audio'
        self.id = id
        self.audio_file_id = audio_file_id
        self.caption = caption
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content
        self.payload_dic['audio_file_id'] = audio_file_id


# Games

class InlineQueryResultGame(JsonSerializable):
    def __init__(self, id, game_short_name, reply_markup=None):
        self.type = 'game'
        self.id = id
        self.game_short_name = game_short_name
        self.reply_markup = reply_markup

    def to_json(self):
        json_dic = {'type': self.type, 'id': self.id, 'game_short_name': self.game_short_name}
        if self.reply_markup:
            json_dic['reply_markup'] = self.reply_markup.to_dic()
        return json.dumps(json_dic)


class Game(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        title = obj['title']
        description = obj['description']
        photo = Game.parse_photo(obj['photo'])
        text = obj.get('text')
        text_entities = None
        if 'text_entities' in obj:
            text_entities = Game.parse_entities(obj['text_entities'])
        animation = None
        if 'animation' in obj:
            animation = Animation.de_json(obj['animation'])
        return cls(title, description, photo, text, text_entities, animation)

    @classmethod
    def parse_photo(cls, photo_size_array):
        ret = []
        for ps in photo_size_array:
            ret.append(PhotoSize.de_json(ps))
        return ret

    @classmethod
    def parse_entities(cls, message_entity_array):
        ret = []
        for me in message_entity_array:
            ret.append(MessageEntity.de_json(me))
        return ret

    def __init__(self, title, description, photo, text=None, text_entities=None, animation=None):
        self.title = title
        self.description = description
        self.photo = photo
        self.text = text
        self.text_entities = text_entities
        self.animation = animation


class Animation(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        file_id = obj['file_id']
        thumb = None
        if 'thumb' in obj:
            thumb = PhotoSize.de_json(obj['thumb'])
        file_name = obj.get('file_name')
        mime_type = obj.get('mime_type')
        file_size = obj.get('file_size')
        return cls(file_id, thumb, file_name, mime_type, file_size)

    def __init__(self, file_id, thumb=None, file_name=None, mime_type=None, file_size=None):
        self.file_id = file_id
        self.thumb = thumb
        self.file_name = file_name
        self.mime_type = mime_type
        self.file_size = file_size


class GameHighScore(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        position = obj['position']
        user = User.de_json(obj['user'])
        score = obj['score']
        return cls(position, user, score)

    def __init__(self, position, user, score):
        self.position = position
        self.user = user
        self.score = score


# Payments

class LabeledPrice(JsonSerializable):
    def __init__(self, label, amount):
        self.label = label
        self.amount = amount

    def to_json(self):
        return json.dumps(self.to_dic())

    def to_dic(self):
        return {'label': self.label, 'amount': self.amount}


class Invoice(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        title = obj['title']
        description = obj['description']
        start_parameter = obj['start_parameter']
        currency = obj['currency']
        total_amount = obj['total_amount']
        return cls(title, description, start_parameter, currency, total_amount)

    def __init__(self, title, description, start_parameter, currency, total_amount):
        self.title = title
        self.description = description
        self.start_parameter = start_parameter
        self.currency = currency
        self.total_amount = total_amount


class ShippingAddress(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        country_code = obj['country_code']
        state = obj['state']
        city = obj['city']
        street_line1 = obj['street_line1']
        street_line2 = obj['street_line2']
        post_code = obj['post_code']
        return cls(country_code, state, city, street_line1, street_line2, post_code)

    def __init__(self, country_code, state, city, street_line1, street_line2, post_code):
        self.country_code = country_code
        self.state = state
        self.city = city
        self.street_line1 = street_line1
        self.street_line2 = street_line2
        self.post_code = post_code


class OrderInfo(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        name = obj.get('name')
        phone_number = obj.get('phone_number')
        email = obj.get('email')
        shipping_address = None
        if 'shipping_address' in obj:
            shipping_address = ShippingAddress.de_json(obj['shipping_address'])
        return cls(name, phone_number, email, shipping_address)

    def __init__(self, name, phone_number, email, shipping_address):
        self.name = name
        self.phone_number = phone_number
        self.email = email
        self.shipping_address = shipping_address


class ShippingOption(JsonSerializable):
    def __init__(self, id, title):
        self.id = id
        self.title = title
        self.prices = []

    def add_price(self, *args):
        """
        Add LabeledPrice to ShippingOption
        :param args: LabeledPrices 
        """
        for price in args:
            self.prices.append(price)

    def to_json(self):
        price_list = []
        for p in self.prices:
            price_list.append(p.to_dic())
        json_dict = json.dumps({'id': self.id, 'title': self.title, 'prices': price_list})
        return json_dict


class SuccessfulPayment(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        currency = obj['currency']
        total_amount = obj['total_amount']
        invoice_payload = obj['invoice_payload']
        shipping_option_id = obj.get('shipping_option_id')
        order_info = None
        if 'order_info' in obj:
            order_info = OrderInfo.de_json(obj['order_info'])
        telegram_payment_charge_id = obj['telegram_payment_charge_id']
        provider_payment_charge_id = obj['provider_payment_charge_id']
        return cls(currency, total_amount, invoice_payload, shipping_option_id, order_info,
                   telegram_payment_charge_id, provider_payment_charge_id)

    def __init__(self, currency, total_amount, invoice_payload, shipping_option_id, order_info,
                 telegram_payment_charge_id, provider_payment_charge_id):
        self.currency = currency
        self.total_amount = total_amount
        self.invoice_payload = invoice_payload
        self.shipping_option_id = shipping_option_id
        self.order_info = order_info
        self.telegram_payment_charge_id = telegram_payment_charge_id
        self.provider_payment_charge_id = provider_payment_charge_id


class ShippingQuery(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        id = obj['id']
        from_user = User.de_json(obj['from'])
        invoice_payload = obj['invoice_payload']
        shipping_address = ShippingAddress.de_json(obj['shipping_address'])
        return cls(id, from_user, invoice_payload, shipping_address)

    def __init__(self, id, from_user, invoice_payload, shipping_address):
        self.id = id
        self.from_user = from_user
        self.invoice_payload = invoice_payload
        self.shipping_address = shipping_address


class PreCheckoutQuery(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        id = obj['id']
        from_user = User.de_json(obj['from'])
        currency = obj['currency']
        total_amount = obj['total_amount']
        invoice_payload = obj['invoice_payload']
        shipping_option_id = obj.get('shipping_option_id')
        order_info = None
        if 'order_info' in obj:
            order_info = OrderInfo.de_json(obj['order_info'])
        return cls(id, from_user, currency, total_amount, invoice_payload, shipping_option_id, order_info)

    def __init__(self, id, from_user, currency, total_amount, invoice_payload, shipping_option_id, order_info):
        self.id = id
        self.from_user = from_user
        self.currency = currency
        self.total_amount = total_amount
        self.invoice_payload = invoice_payload
        self.shipping_option_id = shipping_option_id
        self.order_info = order_info


# Stickers

class StickerSet(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        name = obj['name']
        title = obj['title']
        contains_masks = obj['contains_masks']
        stickers = []
        for s in obj['stickers']:
            stickers.append(Sticker.de_json(s))
        return cls(name, title, contains_masks, stickers)

    def __init__(self, name, title, contains_masks, stickers):
        self.stickers = stickers
        self.contains_masks = contains_masks
        self.title = title
        self.name = name


class Sticker(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        file_id = obj['file_id']
        width = obj['width']
        height = obj['height']
        thumb = None
        if 'thumb' in obj:
            thumb = PhotoSize.de_json(obj['thumb'])
        emoji = obj.get('emoji')
        set_name = obj.get('set_name')
        mask_position = None
        if 'mask_position' in obj:
            mask_position = MaskPosition.de_json(obj['mask_position'])
        file_size = obj.get('file_size')
        return cls(file_id, width, height, thumb, emoji, set_name, mask_position, file_size)

    def __init__(self, file_id, width, height, thumb, emoji, set_name, mask_position, file_size):
        self.file_id = file_id
        self.width = width
        self.height = height
        self.thumb = thumb
        self.emoji = emoji
        self.set_name = set_name
        self.mask_position = mask_position
        self.file_size = file_size


class MaskPosition(JsonDeserializable, JsonSerializable):
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        point = obj['point']
        x_shift = obj['x_shift']
        y_shift = obj['y_shift']
        scale = obj['scale']
        return cls(point, x_shift, y_shift, scale)

    def __init__(self, point, x_shift, y_shift, scale):
        self.point = point
        self.x_shift = x_shift
        self.y_shift = y_shift
        self.scale = scale

    def to_json(self):
        return json.dumps(self.to_dic())

    def to_dic(self):
        return {'point': self.point, 'x_shift': self.x_shift, 'y_shift': self.y_shift, 'scale': self.scale}


class WriteAccessAllowed(JsonDeserializable):
    """
    This object represents a service message about a user allowed to post messages in the chat.
    Currently holds no information.

    Telegram documentation: https://core.telegram.org/bots/api#writeaccessallowed

    :param web_app_name: Optional. Name of the Web App which was launched from a link
    :type web_app_name: :obj:`str`
    """
    @classmethod
    def de_json(cls, json_string):
        if json_string is None: return None
        obj = cls.check_json(json_string)
        return cls(**obj)


    def __init__(self, web_app_name: str) -> None:
        self.web_app_name: str = web_app_name


class InlineQueryResultsButton(JsonSerializable, Dictionaryable):
    """
    This object represents a button to be shown above inline query results.
    You must use exactly one of the optional fields.

    Telegram documentation: https://core.telegram.org/bots/api#inlinequeryresultsbutton

    :param text: Label text on the button
    :type text: :obj:`str`

    :param web_app: Optional. Description of the Web App that will be launched when the user presses the button.
        The Web App will be able to switch back to the inline mode using the method web_app_switch_inline_query inside the Web App.
    :type web_app: :class:`telebot.types.WebAppInfo`

    :param start_parameter: Optional. Deep-linking parameter for the /start message sent to the bot when a user presses the button.
        1-64 characters, only A-Z, a-z, 0-9, _ and - are allowed.
        Example: An inline bot that sends YouTube videos can ask the user to connect the bot to their YouTube account to adapt search
        results accordingly. To do this, it displays a 'Connect your YouTube account' button above the results, or even before showing
        any. The user presses the button, switches to a private chat with the bot and, in doing so, passes a start parameter that instructs
        the bot to return an OAuth link. Once done, the bot can offer a switch_inline button so that the user can easily return to the chat
        where they wanted to use the bot's inline capabilities.
    :type start_parameter: :obj:`str`

    :return: Instance of the class
    :rtype: :class:`InlineQueryResultsButton`
    """

    def __init__(self, text: str, web_app: Optional[WebAppInfo]=None, start_parameter: Optional[str]=None) -> None:
        self.text: str = text
        self.web_app: Optional[WebAppInfo] = web_app
        self.start_parameter: Optional[str] = start_parameter


    def to_dict(self) -> dict:
        json_dict = {
            'text': self.text
        }

        if self.web_app is not None:
            json_dict['web_app'] = self.web_app.to_dict()
        if self.start_parameter is not None:
            json_dict['start_parameter'] = self.start_parameter

        return json_dict

    def to_json(self) -> str:
        return json.dumps(self.to_dict())
