import streamlit as st
import ollama
from agent_logic import get_real_estate_agent_response

# عنوان التطبيق
st.title("وكيل الذكاء الاصطناعي العقاري")

# تهيئة سجل الدردشة في حالة الجلسة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض رسائل الدردشة السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# حقل إدخال المستخدم
if prompt := st.chat_input("كيف يمكنني مساعدتك اليوم؟"): # نص ترحيبي افتراضي
    # إضافة رسالة المستخدم إلى سجل الدردشة وعرضها
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # استدعاء وكيل الذكاء الاصطناعي للحصول على الرد
    # نحتاج إلى تمرير سجل الدردشة الحالي (باستثناء رسالة النظام الأولية) إلى الدالة
    # لكي يتمكن النموذج من الحفاظ على سياق المحادثة.
    # رسالة النظام يتم إضافتها داخل get_real_estate_agent_response
    
    # تصفية رسالة النظام من سجل الدردشة قبل تمريرها
    # ملاحظة: في هذا الإعداد، رسالة النظام يتم إضافتها في كل استدعاء لـ get_real_estate_agent_response
    # لذا لا نحتاج لتمريرها هنا.
    # سنقوم بتمرير سجل الدردشة الفعلي بين المستخدم والوكيل.
    
    # بناء سجل الدردشة للنموذج (بدون رسالة النظام)
    ollama_chat_history = []
    for msg in st.session_state.messages:
        # استبعاد رسالة النظام الافتراضية إذا كانت موجودة في سجل الجلسة
        # والتأكد من أن الرسائل هي من المستخدم أو المساعد
        if msg["role"] in ["user", "assistant"]:
            ollama_chat_history.append(msg)

    response_data = get_real_estate_agent_response(prompt, ollama_chat_history)
    agent_response = response_data["response"]
    should_handover = response_data["should_handover"]

    # عرض رد الوكيل
    with st.chat_message("assistant"):
        st.markdown(agent_response)
    st.session_state.messages.append({"role": "assistant", "content": agent_response})

    # التحقق من الحاجة للتحويل إلى وكيل بشري
    if should_handover:
        st.warning("**ملاحظة:** تم تحويل المحادثة إلى وكيل عقاري بشري. سيتم التواصل معك قريبًا.")
        # هنا يمكنك إضافة منطق إضافي لإرسال إشعار للوكيل البشري
        # أو إعادة تعيين حالة الدردشة لبدء محادثة جديدة.
        # على سبيل المثال، مسح سجل الدردشة لبدء محادثة جديدة بعد التحويل
        # st.session_state.messages = []

# تعليمات تشغيل التطبيق (للمستخدم)
st.sidebar.header("تعليمات التشغيل")
st.sidebar.markdown("1. تأكد من تشغيل تطبيق Ollama في الخلفية.")
st.sidebar.markdown("2. تأكد من سحب النموذج `qwen2:7b` باستخدام `ollama pull qwen2:7b`.")
st.sidebar.markdown("3. افتح Terminal وانتقل إلى مجلد المشروع `real_estate_agent`.")
st.sidebar.markdown("4. قم بتنشيط البيئة الافتراضية: `source venv/bin/activate`.")
st.sidebar.markdown("5. قم بتشغيل التطبيق: `streamlit run app.py`.")
st.sidebar.markdown("6. سيتم فتح التطبيق في متصفح الويب الخاص بك.")
