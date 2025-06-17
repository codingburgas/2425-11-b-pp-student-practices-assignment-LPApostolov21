<section class="max-w-4xl mx-auto p-6 bg-white dark:bg-gray-900 rounded-2xl shadow-md">
  <h1 class="text-3xl font-bold mb-4 text-center text-gray-800 dark:text-white">
    🚗 Car Management & Price Prediction App (Flask)
  </h1>
  <p class="text-gray-700 dark:text-gray-300 text-lg mb-6">
    A full-stack web application built with <strong>Flask</strong> for managing car listings and predicting car prices using machine learning. The app features secure user authentication, an admin dashboard, and a user-friendly interface for submitting car details and receiving price predictions.
  </p>

  <h2 class="text-2xl font-semibold text-gray-800 dark:text-white mb-3">🔧 Features</h2>
  <ul class="list-disc pl-6 text-gray-700 dark:text-gray-300 mb-6 space-y-1">
    <li>🧾 User Registration & Login</li>
    <li>🚙 Add, Edit, Delete Car Records</li>
    <li>📈 Predict Car Price using a trained ML model</li>
    <li>📊 Admin Dashboard to monitor records</li>
    <li>🌓 Dark Mode Support</li>
    <li>🎨 Responsive UI with Bootstrap / Tailwind CSS</li>
  </ul>

  <h2 class="text-2xl font-semibold text-gray-800 dark:text-white mb-3">🧠 Machine Learning</h2>
  <p class="text-gray-700 dark:text-gray-300 mb-3">
    The app uses a trained <strong>Linear Regression</strong> model to predict car prices based on features like:
  </p>
  <ul class="list-disc pl-6 text-gray-700 dark:text-gray-300 mb-6 space-y-1">
    <li>Manifacture Year</li>
    <li>Mileage</li>
  </ul>
  <p class="text-gray-700 dark:text-gray-300 mb-6">
    The model is trained using <strong>scikit-learn</strong> and integrated into the Flask app.
  </p>

 <h2 class="text-2xl font-semibold text-gray-800 dark:text-white mb-3">📁 Project Structure</h2>
<pre class="bg-gray-100 dark:bg-gray-800 text-sm text-gray-800 dark:text-gray-200 p-4 rounded-lg overflow-x-auto">
<code>
project-root/
├── .venv/
├── Documents and diagrams/
├── instance/
│   └── site.db
├── Mech/
│   ├── auth/
│   │   ├── templates/
│   │   ├── __init__.py
│   │   └── routes.py
│   └── main/
│       ├── templates/
│       ├── __init__.py
│       └── routes.py
├── static/
├── app.py
├── forms.py
├── init_db.py
├── models.py
└── README.md
</code>
</pre>

