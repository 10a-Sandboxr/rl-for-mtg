// lib/db.ts
import { Pool } from 'pg';

const ssl =
  process.env.PGSSLMODE === 'require'
    ? { rejectUnauthorized: false }
    : undefined;

const pool = new Pool({
  connectionString: "postgres://neondb_owner:npg_0qomcTlHvr2K@ep-green-waterfall-adgd4miw-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require",
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
