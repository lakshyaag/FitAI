import Link from "next/link";

export default function Home() {
  return (
    <main>
      <div className="hero min-h-screen">
        <div className="hero-content text-center">
          <div className="max-w-md">
            <h1 className="text-5xl font-bold">💪 FitAI</h1>
            <p className="pt-6">
              Elevate your fitness game with a custom workout plan 🏋️‍♀️
            </p>
            <p className="pb-6">
              Just answer a few questions about yourself and jumpstart your
              journey! 🚀
            </p>
            <Link href="/new" className="btn btn-primary">
              Get Started
            </Link>
          </div>
        </div>
      </div>
    </main>
  );
}
