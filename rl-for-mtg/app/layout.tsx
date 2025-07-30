import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Reinforcement Learning for Competitive MTG',
  description: 'Project page for the paper Reinforcement Learning for Competitive Magic: The Gathering Gameplay.',
  openGraph: {
    title: 'RL for Competitive MTG',
    description: 'Project page for the paper Reinforcement Learning for Competitive Magic: The Gathering Gameplay.',
    type: 'website',
  }
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}