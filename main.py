# -*- coding: utf-8 -*-
import voice_assistant
import chat
import voice_generate
import voice_recognize
import hotword_detect
import silence_detect
import vlm

# api参数和模型文件地址
access_key = "***"  # Picovoice访问密钥
keyword_paths = ["***"] # 唤醒词文件路径
model_path = "***"  # 语音识别模型文件路径
stt_access_token = "***" # 百度语音识别访问密钥
tts_access_token = "***"  # 百度语音合成访问密钥
dashscope_api_key = "***" # Dashscope访问密钥

# 初始化唤醒词检测器
detector = hotword_detect.PorcupineWakeWordDetector(access_key, keyword_paths, model_path)
# 初始化音频流
pa = pyaudio.PyAudio()
stream = pa.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=16000,
    input=True,
    frames_per_buffer=1024
)

def main():
    while True:
        # 1. 唤醒词检测
        detector.start()
        
        # 2. 录制用户的语音输入
        status, recorded_audio = voice_assistant.record_audio()
        if not status:
            continue
        audio_file_path = "recorded_audio.wav"
        voice_assistant.save_audio(recorded_audio, audio_file_path)
        
        # 3. 将录音文件转换并进行语音识别
        converted_audio_path = "converted_audio.wav"
        voice_recognize.convert_audio(audio_file_path, converted_audio_path)
        with open(converted_audio_path, 'rb') as audio_file:
            audio_data = audio_file.read()
        recognized_text = voice_recognize.stt(audio_data, stt_access_token)
        print(f"识别的文本: {recognized_text}")
        
        # 4. 使用自然语言处理模块理解用户的意图
        nlp_result = chat.response(recognized_text)
        print(f"NLU结果: {nlp_result}")
        
        # 5. 根据用户的意图生成回复
        if nlp_result["is_understood"]:
            if "play_music" in nlp_result["actions"]:
                response = "好的，我来为你播放音乐。"
                voice_generate.text_to_speech(response, tts_access_token)
                playsound('output.mp3')
                # TODO: 播放音乐
            else:
                if "read_out" in nlp_result["actions"]:
                    # TODO: 拍照片
                    # TODO: 照片上传云端生成链接image_url
                    response = vlm.get_response(dashscope_api_key, image_url, "word_recognition")
                elif "describe" in nlp_result["actions"]:
                    # TODO: 拍照片
                    # TODO: 照片上传云端生成链接image_url
                    response = vlm.get_response(dashscope_api_key, image_url, "image_description")
                elif "add_brightness" in nlp_result["actions"]:
                    # TODO: 调亮灯光
                    response = "好的，我已经调亮了灯光。"
                elif "decrease_brightness" in nlp_result["actions"]:
                    # TODO: 调暗灯光
                    response = "好的，我已经调暗了灯光。"
                voice_generate.text_to_speech(response, tts_access_token)
                playsound('output.mp3')
        else:
            print("对不起，我没有理解你的意思。")
            playsound('error_sound.wav')
            
        sleep(1)  # 暂停一段时间再继续等待唤醒词

if __name__ == "__main__":
    main()
        