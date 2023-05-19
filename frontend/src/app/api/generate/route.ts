import { NextRequest, NextResponse } from 'next/server';

const API_URL = 'https://fitai-backend.onrender.com/generate/';

export async function POST(req: NextRequest) {
  const data = await req.json();
  console.log(data);
  const response = await fetch(API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      answer: data,
    }),
  });
  console.log(response);
  const json = await response.json();
  console.log(json);
  return NextResponse.json(json);
}
