import { NextRequest, NextResponse } from "next/server";

// const API_URL = 'https://fitai-backend.onrender.com/generate/';
const API_URL = "http://localhost:5000/generate";

export async function POST(req: NextRequest) {
  const data = await req.json();
  const response = await fetch(API_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
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
