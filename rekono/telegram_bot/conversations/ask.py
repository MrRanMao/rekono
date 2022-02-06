from typing import List

from processes.models import Process
from projects.models import Project
from targets.models import Target, TargetPort
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import CallbackContext, ConversationHandler
from telegram.update import Update
from telegram_bot.context import PROJECT, TARGET, TOOL
from telegram_bot.conversations.states import (CREATE, EXECUTE,
                                               SELECT_CONFIGURATION,
                                               SELECT_INTENSITY,
                                               SELECT_PROCESS, SELECT_PROJECT,
                                               SELECT_TARGET,
                                               SELECT_TARGET_PORT, SELECT_TOOL)
from telegram_bot.messages.ask import (ASK_FOR_CONFIGURATION,
                                       ASK_FOR_INTENSITY, ASK_FOR_PROCESS,
                                       ASK_FOR_PROJECT, ASK_FOR_TARGET,
                                       ASK_FOR_TARGET_PORT, ASK_FOR_TOOL,
                                       NO_PROCESSES, NO_PROJECTS,
                                       NO_TARGET_PORTS, NO_TARGETS)
from telegram_bot.messages.execution import confirmation_message
from telegram_bot.models import TelegramChat
from tools.enums import IntensityRank
from tools.models import Configuration, Tool


def send_message(update: Update, chat: TelegramChat, text: str) -> None:
    '''Send Telegram text message.

    Args:
        update (Update): Telegram Bot update
        chat (TelegramChat): Telegram chat entity
        text (str): Text message to send
    '''
    if hasattr(update, 'message') and getattr(update, 'message'):               # Standard update
        update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN_V2)
    else:                                                                       # Update from keyboard selection
        update.callback_query.bot.send_message(chat.chat_id, text=text, parse_mode=ParseMode.MARKDOWN_V2)


def send_options(update: Update, chat: TelegramChat, text: str, keyboard: List[List[InlineKeyboardButton]]) -> None:
    '''Send Telegram options message.

    Args:
        update (Update): Telegram Bot update
        chat (TelegramChat): Telegram chat entity
        text (str): Text message to send
        keyboard (List[List[InlineKeyboardButton]]): Keyboard with the available options
    '''
    if hasattr(update, 'message') and getattr(update, 'message'):               # Standard update
        update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN_V2)
    else:                                                                       # Update from keyboard selection
        update.callback_query.bot.send_message(chat.chat_id, text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN_V2)


def ask_for_project(update: Update, context: CallbackContext, chat: TelegramChat) -> int:
    '''Ask the user for choose one project.

    Args:
        update (Update): Telegram Bot update
        chat (TelegramChat): Telegram chat entity

    Returns:
        int: Next conversation state or end conversation
    '''
    projects = Project.objects.filter(members=chat.user).order_by('name').all()     # Get all user projects
    if not projects:                                                            # No projects found
        send_message(update, chat, NO_PROJECTS)
        return ConversationHandler.END                                          # End conversation
    else:
        # Build keyboard with the projects data
        keyboard = [[InlineKeyboardButton(p.name, callback_data=p.id) for p in projects]]
        send_options(update, chat, ASK_FOR_PROJECT, keyboard)
        return SELECT_PROJECT                                                   # Go to next conversation state


def ask_for_target(update: Update, context: CallbackContext, chat: TelegramChat) -> int:
    '''Ask the user for choose one target.

    Args:
        update (Update): Telegram Bot update
        chat (TelegramChat): Telegram chat entity

    Returns:
        int: Next conversation state or end conversation
    '''
    targets = Target.objects.filter(project=context.chat_data[PROJECT]).order_by('target').all()  # Get all user targets
    if not targets:                                                             # No projects found
        send_message(update, chat, NO_TARGETS)
        return ConversationHandler.END                                          # End conversation
    else:
        # Build keyboard with the targets data
        keyboard = [[InlineKeyboardButton(t.target, callback_data=t.id) for t in targets]]
        send_options(update, chat, ASK_FOR_TARGET, keyboard)
        return SELECT_TARGET                                                    # Go to next conversation state


def ask_for_target_port(update: Update, context: CallbackContext, chat: TelegramChat) -> int:
    '''Ask the user for choose one target port.

    Args:
        update (Update): Telegram Bot update
        chat (TelegramChat): Telegram chat entity

    Returns:
        int: Next conversation state or end conversation
    '''
    target_ports = TargetPort.objects.filter(target=context.chat_data[TARGET]).order_by('port').all()     # Get target ports
    if not target_ports:                                                        # No target ports found
        send_message(update, chat, NO_TARGET_PORTS)
        return ConversationHandler.END                                          # End conversation
    else:
        # Build keyboard with the target ports data
        keyboard = [[InlineKeyboardButton(tp.port, callback_data=tp.id) for tp in target_ports]]
        send_options(update, chat, ASK_FOR_TARGET_PORT, keyboard)
        return SELECT_TARGET_PORT                                                       # Go to next conversation state


def ask_for_process(update: Update, context: CallbackContext, chat: TelegramChat) -> int:
    '''Ask the user for choose one process.

    Args:
        update (Update): Telegram Bot update
        chat (TelegramChat): Telegram chat entity

    Returns:
        int: Next conversation state or end conversation
    '''
    processes = Process.objects.order_by('name').all()
    if not processes:
        send_message(update, chat, NO_PROCESSES)
        return ConversationHandler.END                                          # End conversation
    else:
        # Build keyboard with the processes data
        keyboard = [[InlineKeyboardButton(p.name, callback_data=p.id) for p in processes]]
        send_options(update, chat, ASK_FOR_PROCESS, keyboard)
        return SELECT_PROCESS                                                    # Go to next conversation state


def ask_for_tool(update: Update, context: CallbackContext, chat: TelegramChat) -> int:
    '''Ask the user for choose one tool.

    Args:
        update (Update): Telegram Bot update
        chat (TelegramChat): Telegram chat entity

    Returns:
        int: Next conversation state or end conversation
    '''
    tools = Tool.objects.order_by('name').all()
    # Build keyboard with the tools data
    keyboard = [[InlineKeyboardButton(t.name, callback_data=t.id) for t in tools]]
    send_options(update, chat, ASK_FOR_TOOL, keyboard)
    return SELECT_TOOL                                                          # Go to next conversation state


def ask_for_configuration(update: Update, context: CallbackContext, chat: TelegramChat) -> int:
    '''Ask the user for choose one configuration.

    Args:
        update (Update): Telegram Bot update
        chat (TelegramChat): Telegram chat entity

    Returns:
        int: Next conversation state or end conversation
    '''
    configurations = Configuration.objects.filter(tool=context.chat_data[TOOL]).order_by('name').all()
    # Build keyboard with the configurations data
    keyboard = [[InlineKeyboardButton(c.name, callback_data=c.id) for c in configurations]]
    send_options(update, chat, ASK_FOR_CONFIGURATION, keyboard)
    return SELECT_CONFIGURATION                                                 # Go to next conversation state


def ask_for_intensity(update: Update, context: CallbackContext, chat: TelegramChat) -> int:
    '''Ask the user for choose one intensity.

    Args:
        update (Update): Telegram Bot update
        chat (TelegramChat): Telegram chat entity

    Returns:
        int: Next conversation state or end conversation
    '''
    intensities = IntensityRank.names
    if TOOL in context.chat_data:
        intensities = [IntensityRank(i.value).name for i in context.chat_data[TOOL].intensities.order_by('value').all()]
    intensities.reverse()
    keyboard = [[InlineKeyboardButton(i.capitalize(), callback_data=i) for i in intensities]]
    send_options(update, chat, ASK_FOR_INTENSITY, keyboard)
    return SELECT_INTENSITY                                                     # Go to next conversation state


def ask_for_execution_confirmation(update: Update, context: CallbackContext, chat: TelegramChat) -> int:
    '''Ask the user for confirmation.

    Args:
        update (Update): Telegram Bot update
        chat (TelegramChat): Telegram chat entity

    Returns:
        int: Next conversation state or end conversation
    '''
    keyboard = [[
        InlineKeyboardButton('Yes', callback_data='yes'),
        InlineKeyboardButton('No', callback_data='no')
    ]]
    send_options(update, chat, confirmation_message(context), keyboard)
    return EXECUTE                                                           # Go to next conversation state
