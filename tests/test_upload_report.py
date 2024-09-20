import unittest
from app import create_app
from flask import url_for

class TestUploadReport(unittest.TestCase):

    def setUp(self):
        # إعداد التطبيق للاختبار
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def login(self, email_or_id, password):
        # تأكد من تمرير القيم الصحيحة وعدم تمرير قيم فارغة
        if not email_or_id or not password:
            raise ValueError("Both email_or_id and password must be provided")
        
        # تأكد من أن البيانات المرسلة صحيحة
        return self.client.post('/login', data={
            'email_or_id': email_or_id,
            'password': password
        }, follow_redirects=True)

    def test_upload_report(self):
        # إجراء تسجيل الدخول باستخدام بيانات صحيحة
        email_or_id = 'test@example.com'  # تأكد من أن هذا حقل صحيح في النموذج
        password = 'password'  # تأكد من أن كلمة المرور صحيحة

        # إجراء طلب تسجيل الدخول
        login_response = self.login(email_or_id, password)

        # تحقق من حالة الرد (تأكد من أن تسجيل الدخول تم بنجاح)
        self.assertEqual(login_response.status_code, 200)

        # اختبارات إضافية بعد تسجيل الدخول
        # مثال: تحميل تقرير
        response = self.client.post('/upload_report', data={
            'report_data': 'Test report data'
        }, follow_redirects=True)

        # تحقق من حالة الرد بعد رفع التقرير
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Report uploaded successfully', response.data)

if __name__ == '__main__':
    unittest.main()
