import asyncio
import socketio
import pandas as pd
import logging
import random

# ตั้งค่า logging
logging.basicConfig(encoding='utf-8', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

BASE_WEBSOCKET_URL = "ENTER_YOUR_WEBSOCKET_URL_HERE"
cost_per_request = 0.05
total_cost = 0

# กำหนด username ที่ต้องการใช้
USERNAME = "ENTER_YOUR_USERNAME_HERE"
PROJECT = "ENTER_YOUR_PROJECT_NAME_HERE"

# อ่านคำถามจาก Excel โดยปรับเงื่อนไขการเลือก
def load_questions(file_path, sample_size=100, max_questions_per_ref=10):
    try:
        df = pd.read_excel(file_path, header=0)  # ใช้ header
        df = df.fillna('')  # แทนค่าว่างด้วย ''

        # ตรวจสอบว่ามีคอลัมน์ที่ต้องการ
        if "question" not in df.columns or "ref" not in df.columns:
            logging.error("Missing required columns: 'question' and 'ref'")
            return []

        # ลบ 'file_name': ออกจาก ref เพื่อใช้เป็น key
        df["ref"] = df["ref"].astype(str).str.replace("'file_name': ", "", regex=False)

        sampled_questions = []

        # กลุ่มคำถามตาม ref
        grouped = df.groupby("ref")

        # ดึงรายการ ref ทั้งหมดและทำการสุ่มลำดับ
        refs = list(grouped.groups.keys())
        random.shuffle(refs)  # สุ่มลำดับของ refs

        for ref in refs:
            group = grouped.get_group(ref)

            # เลือกคำถามที่ไม่ซ้ำกันและไม่ว่างเปล่า
            unique_questions = group["question"].drop_duplicates().str.strip()
            unique_questions = unique_questions[unique_questions != '']

            num_questions = len(unique_questions)

            if num_questions >= max_questions_per_ref:
                # เลือกจำนวนคำถามสูงสุดที่กำหนด (10)
                selected = unique_questions.sample(n=max_questions_per_ref, random_state=random.randint(0, 10000)).tolist()
            elif num_questions > 0:
                # เลือกทุกคำถามที่มีอยู่ถ้าน้อยกว่า max แต่มากกว่า 0
                selected = unique_questions.tolist()
            else:
                # ข้าม `ref` หากไม่มีคำถามเลย
                logging.warning(f"[Ref: {ref}] ไม่มีคำถามเลย จะถูกข้ามไป")
                continue

            # เก็บทั้ง ref และคำถาม
            sampled_questions.extend([(ref, q) for q in selected])

            # ตรวจสอบว่าเกิน sample_size หรือไม่
            if len(sampled_questions) >= sample_size:
                break

        return sampled_questions[:sample_size]
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        return []

async def send_question(sio, username, project, ref, question):
    global total_cost
    try:
        payload = {"question": question, "username": username, "project": project}

        def on_ask_chat_response(*args):
            if args:
                response = args[0]
                if response == "success":
                    logging.info(f"[Ref: {ref}] ส่งคำถาม: '{question}' - สถานะ: สำเร็จ")
                else:
                    logging.error(f"[Ref: {ref}] ส่งคำถาม: '{question}' - สถานะ: ล้มเหลว, Response: {response}")
            else:
                logging.error(f"[Ref: {ref}] ส่งคำถาม: '{question}' - ไม่ได้รับการตอบสนองจากเซิร์ฟเวอร์")

        logging.info(f"[Ref: {ref}] กำลังส่งคำถาม: '{question}'...")
        await sio.emit("ask_chat", payload, callback=on_ask_chat_response)
        total_cost += cost_per_request
        await asyncio.sleep(2)  # หน่วงเวลาเล็กน้อย
    except Exception as e:
        logging.error(f"[Ref: {ref}] เกิดข้อผิดพลาดสำหรับ {username}: {e}")

async def main():
    excel_file = r"ENTER_YOUR_EXCEL_FILE_PATH_HERE"
    sample_size = 100  # จำนวนคำถามที่ต้องการ
    questions = load_questions(excel_file, sample_size=sample_size, max_questions_per_ref=10)

    if not questions:
        logging.error("ไม่พบคำถามใดๆ. จึงหยุดการทำงาน...")
        return

    sio = socketio.AsyncClient()

    @sio.event
    def connect():
        logging.info("เชื่อมต่อกับ WebSocket สำเร็จแล้ว!")

    @sio.event
    def disconnect():
        logging.info("ตัดการเชื่อมต่อกับ WebSocket.")

    try:
        logging.info("กำลังเชื่อมต่อกับ WebSocket...")
        await sio.connect(BASE_WEBSOCKET_URL)

        # ส่งคำถามทีละตัว
        for ref, question in questions:
            await send_question(sio, USERNAME, PROJECT, ref, question)

    except socketio.exceptions.ConnectionError as e:
        logging.error(f"เกิดข้อผิดพลาดในการเชื่อมต่อ: {e}")
    except Exception as e:
        logging.error(f"เกิดข้อผิดพลาดระหว่างการทำงาน: {e}")

    finally:
        logging.info("กำลังตัดการเชื่อมต่อ WebSocket...")
        await sio.disconnect()
        logging.info(f"ต้นทุนทั้งหมด: ${total_cost:.2f} สำหรับ {len(questions)} คำถาม.")

if __name__ == "__main__":
    asyncio.run(main())
