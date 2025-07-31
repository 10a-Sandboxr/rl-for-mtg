// app/api/log/route.ts
export const runtime = 'nodejs';

import { NextResponse } from 'next/server';
import { query } from '@/lib/db';

type Payload = {
  method: string;
  pathname: string;
  search?: string | null;
  ip?: string | null;
  ua?: string | null;
};

export async function POST(req: Request) {
  try {
    const body = (await req.json()) as Payload;

    // Basic shape check
    if (!body || !body.method || !body.pathname) {
      return NextResponse.json({ ok: false, error: 'bad_request' }, { status: 400 });
    }

    await query(
      `
      INSERT INTO rlmtg_paths (method, pathname, search, ip, ua)
      VALUES ($1, $2, $3, $4::inet, $5)
      `,
      [
        body.method,
        body.pathname,
        body.search ?? null,
        body.ip ?? null,
        body.ua ?? null,
      ]
    );

    return NextResponse.json({ ok: true }, { status: 201 });
  } catch (err) {
    console.error('[log][insert]', err);
    return NextResponse.json({ ok: false }, { status: 500 });
  }
}
