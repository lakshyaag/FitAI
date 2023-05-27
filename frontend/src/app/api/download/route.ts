import { NextRequest, NextResponse } from "next/server";
import puppeteer from "puppeteer";

const saveAsPDF = async (planId: string) => {
  const BASE_URL = "http://localhost:3000/result?";
  // const BASE_URL = "https://fit-ai-omega.vercel.app/result?";
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();

  await page.goto(BASE_URL + planId, {
    waitUntil: "networkidle0",
  });

  const result = await page.pdf({
    format: "a4",
  });

  await browser.close();

  return result;
};

export async function POST(req: NextRequest) {
  const { planId } = await req.json();

  const pdf = await saveAsPDF(planId);

  const res = new NextResponse(pdf);

  res.headers.set("Content-Disposition", `attachment; filename=FitAI.pdf`);
  res.headers.set("Content-Type", "application/pdf");

  //   return res.send(pdf);
  return res;
}
