import '../styles/globals.css';
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'SecureTask Manager',
  description: 'Professional task management with advanced security and real-time collaboration',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={`${inter.className} bg-gradient-to-br from-blue-50 to-indigo-50`}>
        <div className="min-h-screen">
          {/* Header will be conditionally rendered based on authentication */}
          <main className="container mx-auto py-6 px-4">
            <div className="animate-fadeIn">
              {children}
            </div>
          </main>
        </div>
      </body>
    </html>
  );
}