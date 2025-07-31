// middleware.ts
import type { NextRequest } from 'next/server';
import { NextResponse } from 'next/server';

export async function middleware(req: NextRequest) {
  const { nextUrl, method, headers } = req;
  const pathname = nextUrl.pathname;         // e.g., /, /foo, /foo/bar
  const search = nextUrl.search || '';       // e.g., ?q=mtg&page=2 ('' if none)

  // Skip internal/asset paths to avoid noise and recursion
  if (
    pathname.startsWith('/_next') ||
    pathname.startsWith('/api/log') ||
    pathname === '/favicon.ico' ||
    pathname === '/robots.txt' ||
    pathname === '/sitemap.xml'
  ) {
    return NextResponse.next();
  }

  const ip =
    req.ip ??
    headers.get('x-forwarded-for')?.split(',')[0]?.trim() ??
    null;
  const ua = headers.get('user-agent') ?? null;

  // Fire-and-forget (do not block the request)
  // Note: we intentionally do not await this fetch
  // eslint-disable-next-line @typescript-eslint/no-floating-promises
  fetch(new URL('/api/log', nextUrl.origin), {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ method, pathname, search, ip, ua }),
  }).catch(() => { /* swallow logging errors */ });

  return NextResponse.next();
}

// Match everything; we filter exclusions in the function above.
export const config = {
  matcher: ['/:path*'],
};
