import ollama

def get_real_estate_agent_response(user_message: str, chat_history: list) -> dict:
    """
    يتفاعل مع نموذج Ollama LLM لإنشاء استجابة وكيل عقاري.
    يحتوي على منطق لتحديد ما إذا كان يجب تحويل العميل إلى وكيل بشري.
    """

    # تعريف البرومبت الخاص بالنظام لوكيل الذكاء الاصطناعي العقاري
    system_prompt = """
    أنت مساعد عقاري ذكي وودود لشركة عقارية. مهمتك هي مساعدة العملاء في استفساراتهم المتعلقة بالشراء أو الإيجار.
    تفاعل مع العملاء بأسلوب احترافي وودود، واجمع المعلومات الأساسية منهم.

    **الهدف الأساسي:**
    1.  فهم ما إذا كان العميل يبحث عن شراء أو إيجار عقار.
    2.  جمع تفاصيل مهمة مثل: نوع العقار (شقة، فيلا، أرض، تجاري)، الموقع/المنطقة المفضلة، الميزانية (سعر الشراء أو الإيجار الشهري)، عدد غرف النوم/الحمامات، وأي متطلبات خاصة أخرى.
    3.  تحديد متى يجب تحويل المحادثة إلى وكيل عقاري بشري.

    **معايير التحويل إلى وكيل بشري:**
    *   إذا طلب العميل صراحة التحدث إلى وكيل بشري.
    *   إذا كانت استفسارات العميل معقدة للغاية أو تتطلب تفاوضًا أو استشارة شخصية لا يمكن للذكاء الاصطناعي التعامل معها.
    *   إذا أبدى العميل اهتمامًا جادًا بمعاينة عقار أو طلب معلومات حساسة.
    *   إذا تم جمع المعلومات الأساسية (النوع، الموقع، الميزانية) وكان العميل مستعدًا للخطوة التالية.

    **عند التحويل، يجب أن تقول بوضوح:** "يبدو أن استفسارك يتطلب تدخل وكيل عقاري بشري. سأقوم بتحويلك إلى أحد خبرائنا الآن لمساعدتك بشكل أفضل." ثم قم بإنهاء المحادثة من جانبك.

    **تعليمات إضافية:**
    *   حافظ على الردود موجزة ومباشرة قدر الإمكان.
    *   استخدم اللغة التي يتحدث بها العميل (العربية أو الإنجليزية).
    *   إذا لم تكن متأكدًا من كيفية الرد، اطلب المزيد من التوضيح أو اقترح التحويل إلى وكيل بشري.
    *   لا تقدم وعودًا أو معلومات غير مؤكدة.
    *   لا تطلب معلومات شخصية حساسة مثل أرقام الهوية أو تفاصيل الحسابات البنكية.

    ابدأ دائمًا بتحية ودودة وسؤال مفتوح لتشجيع العميل على وصف احتياجاته.
    """

    # بناء رسائل المحادثة
    messages = [
        {"role": "system", "content": system_prompt}
    ] + chat_history + [
        {"role": "user", "content": user_message}
    ]

    try:
        # استدعاء نموذج Ollama (باستخدام qwen2:7b كما تم تحديده مسبقًا)
        response = ollama.chat(model='qwen2:7b', messages=messages)
        agent_response_content = response['message']['content']

        # منطق بسيط لتحديد التحويل بناءً على كلمات مفتاحية في رد النموذج
        # يمكن تحسين هذا المنطق لاحقًا باستخدام تحليل المشاعر أو استخراج الكيانات
        if "تحويلك إلى أحد خبرائنا" in agent_response_content or \
           "human agent" in agent_response_content.lower() or \
           "speak to a representative" in agent_response_content.lower():
            should_handover = True
        else:
            should_handover = False

        return {
            "response": agent_response_content,
            "should_handover": should_handover
        }

    except Exception as e:
        print(f"حدث خطأ أثناء التفاعل مع Ollama: {e}")
        return {
            "response": "عذرًا، حدث خطأ فني. يرجى المحاولة مرة أخرى لاحقًا أو الاتصال بنا مباشرة.",
            "should_handover": True # في حالة الخطأ، من الأفضل التحويل لوكيل بشري
        }

if __name__ == '__main__':
    # مثال على كيفية استخدام الوكيل
    print("وكيل الذكاء الاصطناعي العقاري (محلي)")
    print("اكتب 'exit' للخروج أو 'handover' للتحويل إلى وكيل بشري.")

    current_chat_history = []

    while True:
        user_input = input("أنت: ")
        if user_input.lower() == 'exit':
            break
        if user_input.lower() == 'handover':
            print("الوكيل: يبدو أن استفسارك يتطلب تدخل وكيل عقاري بشري. سأقوم بتحويلك إلى أحد خبرائنا الآن لمساعدتك بشكل أفضل.")
            break

        response_data = get_real_estate_agent_response(user_input, current_chat_history)
        agent_reply = response_data["response"]
        should_handover = response_data["should_handover"]

        print(f"الوكيل: {agent_reply}")

        current_chat_history.append({"role": "user", "content": user_input})
        current_chat_history.append({"role": "assistant", "content": agent_reply})

        if should_handover:
            print("--- تم التحويل إلى وكيل بشري ---")
            break
