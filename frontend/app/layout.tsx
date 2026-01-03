import "./globals.css";
import Navbar from "@/components/Navbar";

export const metadata = {
  title: "CP Mentor",
  description: "AI-powered Competitive Programming Mentor"
};

export default function RootLayout({
  children
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <Navbar />
        <main>{children}</main>
      </body>
    </html>
  );
}