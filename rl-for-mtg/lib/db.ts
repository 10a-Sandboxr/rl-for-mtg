// lib/db.ts
import { Pool } from 'pg';

const ssl =
  process.env.PGSSLMODE === 'require'
    ? { rejectUnauthorized: false }
    : undefined;

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl,
  // keep tiny for serverless; tune if you run a long-lived server
  max: 3,
});

export async function query<T = any>(text: string, params?: any[]) {
  const client = await pool.connect();
  try {
    const res = await client.query(text, params);
    return res;
  } finally {
    client.release();
  }
}
