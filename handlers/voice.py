import json
import os
import subprocess
from pathlib import Path

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from vosk import KaldiRecognizer, Model

from keyboards import keyboards as kb
from main import dp, bot


class VoiceToText(StatesGroup):
    voice_to_text = State()


class STT:
    # Перелік доступних моделей
    MODELS = {
        "english": "handlers/models/vosk/vosk-model-en",
        "ukrainian": "handlers/models/vosk/vosk-model-uk"
    }

    default_init = {
        "sample_rate": 16000,
        "ffmpeg_path": "handlers/models/vosk"  # путь к ffmpeg
    }

    def __init__(self,
                 language="english",
                 sample_rate=None,
                 ffmpeg_path=None
                 ) -> None:
        """
        Настройка модели Vosk для распознования аудио и
        преобразования его в текст.
        :param language: str  мова для моделі (english або ukrainian)
        :param sample_rate: int  частота выборки, обычно 16000
        :param ffmpeg_path: str  путь к ffmpeg
        """
        if language not in STT.MODELS:
            raise ValueError("Недоступна мова. Доступні мови: english, ukrainian")

        self.model_path = STT.MODELS[language]
        self.sample_rate = sample_rate if sample_rate else STT.default_init["sample_rate"]
        self.ffmpeg_path = ffmpeg_path if ffmpeg_path else STT.default_init["ffmpeg_path"]

        self._check_model()

        model = Model(self.model_path)
        self.recognizer = KaldiRecognizer(model, self.sample_rate)
        self.recognizer.SetWords(True)

    def _check_model(self):
        """
        Проверка наличия модели Vosk на нужном языке в каталоге приложения
        """
        if not os.path.exists(self.model_path):
            raise Exception(
                "Vosk: сохраните папку model в папку vosk\n"
                "Скачайте модель по ссылке https://alphacephei.com/vosk/models"
            )

        isffmpeg_here = False
        for file in os.listdir(self.ffmpeg_path):
            if file.startswith('ffmpeg'):
                isffmpeg_here = True

        if not isffmpeg_here:
            raise Exception(
                "Ffmpeg: сохраните ffmpeg.exe в папку ffmpeg\n"
                "Скачайте ffmpeg.exe по ссылке https://ffmpeg.org/download.html"
            )
        self.ffmpeg_path = self.ffmpeg_path + '/ffmpeg'

    def audio_to_text(self, audio_file_name=None) -> str:
        """
        Offline-распознавание аудио в текст через Vosk
        :param audio_file_name: str путь и имя аудио файла
        :return: str распознанный текст
        """
        if audio_file_name is None:
            raise Exception("Укажите путь и имя файла")
        if not os.path.exists(audio_file_name):
            raise Exception("Укажите правильный путь и имя файла")

        # Конвертация аудио в wav и результат в process.stdout
        process = subprocess.Popen(
            [self.ffmpeg_path,
             "-loglevel", "quiet",
             "-i", audio_file_name,
             "-ar", str(self.sample_rate),
             "-ac", "1",
             "-f", "s16le",
             "-"
             ],
            stdout=subprocess.PIPE
        )

        while True:
            data = process.stdout.read(4000)
            if len(data) == 0:
                break
            if self.recognizer.AcceptWaveform(data):
                pass

        result_json = self.recognizer.FinalResult()
        result_dict = json.loads(result_json)
        return result_dict["text"]


@dp.message_handler(content_types=[
    types.ContentType.VOICE,
    types.ContentType.AUDIO,
    types.ContentType.DOCUMENT
])
async def voice_message_handler(message: types.Message, state: FSMContext):
    global current_language
    if message.content_type == types.ContentType.VOICE:
        file_id = message.voice.file_id
    elif message.content_type == types.ContentType.AUDIO:
        file_id = message.audio.file_id
    elif message.content_type == types.ContentType.DOCUMENT:
        file_id = message.document.file_id
    else:
        await message.reply("Формат документа не підтримується")
        return

    await message.reply('Вкажіть мову голосового!', reply_markup=kb.lang_keyboard)

    await state.update_data(file_id=file_id)
    await VoiceToText.voice_to_text.set()


@dp.callback_query_handler(lambda callback_query: callback_query.data in ["lang_english", "lang_ukrainian"],
                           state=VoiceToText.voice_to_text)
async def choose_language(call: types.CallbackQuery, state: FSMContext):
    global stt, current_language
    data = await state.get_data()

    if call.data.split("_")[1] == "english":
        current_language = "🇬🇧"
    elif call.data.split("_")[1] == "ukrainian":
        current_language = "🇺🇦"

    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f"Обрана мова: {current_language}")
    await bot.send_chat_action(chat_id=call.message.chat.id, action='typing')

    stt = STT(language=call.data.split("_")[1])  # Вибираємо модель для англійської мови

    file_id = data.get('file_id')

    file = await bot.get_file(file_id)
    file_path = file.file_path
    file_on_disk = Path("", f"{file_id}.tmp")
    await bot.download_file(file_path, destination=file_on_disk)

    text = stt.audio_to_text(file_on_disk)

    if not text:
        text = "Формат документа не підтримується!"
    await call.message.reply(text)

    os.remove(file_on_disk)  # Удаление временного файла
    await state.finish()

    return
