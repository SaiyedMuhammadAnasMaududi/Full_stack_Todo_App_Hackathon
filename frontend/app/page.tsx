'use client';

import { useRouter } from 'next/navigation';
import Link from 'next/link';
import Header from '@/components/Header/Header';

export default function HomePage() {
  const router = useRouter();

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />

      <main className="main-content mx-auto py-6 px-4">
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-extrabold text-gray-900 mb-4">
            Boost Your Productivity with Our Todo App
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Organize your tasks, manage your time, and achieve your goals with our intuitive and secure todo application.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-12 items-center mb-16">
          <div>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">What is a Todo App?</h2>
            <p className="text-gray-600 mb-4">
              A todo app is a digital task management tool that helps you organize, prioritize, and track your daily activities.
              It transforms scattered thoughts and commitments into a structured, manageable system that enhances productivity and reduces stress.
            </p>
            <p className="text-gray-600">
              Our secure todo app provides a centralized platform where you can capture ideas, set deadlines, and monitor progress -
              all while maintaining the privacy and security of your personal information.
            </p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold text-gray-900 mb-4">Best Practices for Using Todo Apps</h3>
            <ul className="space-y-3">
              <li className="flex items-start">
                <span className="text-green-500 mr-2">✓</span>
                <span className="text-gray-700"><strong>Prioritize tasks:</strong> Use urgency/importance matrix to focus on what matters most</span>
              </li>
              <li className="flex items-start">
                <span className="text-green-500 mr-2">✓</span>
                <span className="text-gray-700"><strong>Break big tasks:</strong> Divide large projects into smaller, actionable steps</span>
              </li>
              <li className="flex items-start">
                <span className="text-green-500 mr-2">✓</span>
                <span className="text-gray-700"><strong>Set deadlines:</strong> Attach realistic due dates to maintain momentum</span>
              </li>
              <li className="flex items-start">
                <span className="text-green-500 mr-2">✓</span>
                <span className="text-gray-700"><strong>Review regularly:</strong> Schedule weekly reviews to reassess priorities</span>
              </li>
              <li className="flex items-start">
                <span className="text-green-500 mr-2">✓</span>
                <span className="text-gray-700"><strong>Capture quickly:</strong> Record tasks immediately to prevent mental overload</span>
              </li>
            </ul>
          </div>
        </div>

        <div className="bg-gradient-to-r from-blue-500 to-indigo-600 rounded-2xl p-8 md:p-12 text-white text-center">
          <h2 className="text-2xl md:text-3xl font-bold mb-4">Ready to Transform Your Productivity?</h2>
          <p className="text-blue-100 mb-6 max-w-2xl mx-auto">
            Join thousands of users who have streamlined their workflow and achieved their goals with our secure, intuitive todo application.
          </p>

          <div className="flex flex-col sm:flex-row justify-center gap-4">
            <Link
              href="/signup"
              className="px-8 py-3 bg-white text-blue-600 font-semibold rounded-lg shadow-md hover:bg-gray-100 transition-colors duration-200"
            >
              Create Account
            </Link>
            <Link
              href="/login"
              className="px-8 py-3 bg-transparent border-2 border-white text-white font-semibold rounded-lg hover:bg-white hover:bg-opacity-10 transition-colors duration-200"
            >
              Sign In
            </Link>
          </div>
        </div>

        <div className="mt-16 grid md:grid-cols-3 gap-8">
          <div className="text-center p-6 bg-white rounded-lg shadow-sm">
            <div className="text-blue-500 text-3xl mb-4">✓</div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Secure & Private</h3>
            <p className="text-gray-600">Your data is encrypted and protected with industry-leading security measures.</p>
          </div>

          <div className="text-center p-6 bg-white rounded-lg shadow-sm">
            <div className="text-blue-500 text-3xl mb-4">✓</div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Cross-Device Sync</h3>
            <p className="text-gray-600">Access your tasks seamlessly across all your devices.</p>
          </div>

          <div className="text-center p-6 bg-white rounded-lg shadow-sm">
            <div className="text-blue-500 text-3xl mb-4">✓</div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Intuitive Design</h3>
            <p className="text-gray-600">Clean, user-friendly interface designed for maximum productivity.</p>
          </div>
        </div>
      </main>

      <footer className="bg-white border-t border-gray-200 py-8 mt-12">
        <div className="main-content mx-auto px-4 text-center text-gray-600">
          <p>© 2026 Todo App. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}