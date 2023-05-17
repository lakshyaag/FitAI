import { getWorkoutPlan } from "@/utils"
import Link from "next/link"

export default function Home() {
  const dummyData = {
    answer: {
      "1": "18-24",
      "2": "Male",
      "3": 180,
      "4": 79,
      "5": "Beginner",
      "6": "No",
      "7": "4 days",
      "8": "Gain muscle",
      "9": "Gym",
      "10": "Arms",
      "11": "Full-body workouts",
      "12": "Bodyweight exercises",
      "13": "No",
      "14": "",
      "15": "Less than 30 minutes",
      "16": ["Dumbbells", "Barbells"],
      "17": "",
      "18": "3 months",
    },
  }

  getWorkoutPlan(dummyData)
    .then((data) => {
      console.log(data)
    })
    .catch((err) => {
      console.log(err)
    })

  return (
    <main>
      <div className="hero min-h-screen bg-base-200">
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
  )
}
