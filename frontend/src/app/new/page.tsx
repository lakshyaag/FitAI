"use client"

import { NextPage } from "next"
import { FC, useEffect, useState } from "react"

import questionsFile from "../../questions.json"
import { getWorkoutPlan } from "@/utils"

const { questions } = questionsFile as {
  questions: Question[]
}

interface Question {
  id: number
  section: FormSection
  text: string
  options: string[]
  question_type:
    | "single_select"
    | "numeric_input"
    | "multi_select"
    | "text_input"
}

type FormSection =
  | "Personal Information"
  | "Fitness History"
  | "Goals & Preferences"
  | "Physical Constraints"
const formSections: FormSection[] = [
  "Personal Information",
  "Fitness History",
  "Goals & Preferences",
  "Physical Constraints",
]
const sectionBreakpoints = {
  "Personal Information": 1,
  "Fitness History": 5,
  "Goals & Preferences": 8,
  "Physical Constraints": 17,
}

const Question: FC<{
  question: Question
  isLast: boolean
  onClickNext: (answer: string | string[]) => void
}> = ({ question, isLast, onClickNext }) => {
  const [answer, setAnswer] = useState<string | string[]>(
    question.question_type === "multi_select"
      ? []
      : question.options?.[0] || "N/A"
  )

  const handleCheckboxChange = (option: string) => {
    if (answer.includes(option)) {
      // Remove the option if it's already selected
      setAnswer((prevAnswer) =>
        (prevAnswer as string[]).filter(
          (selectedOption) => selectedOption !== option
        )
      )
    } else {
      // Add the option if it's not selected
      setAnswer((prevAnswer) => [...(prevAnswer as string[]), option])
    }
  }

  useEffect(() => {
    if (question.question_type === "single_select") {
      setAnswer(question.options?.[0])
    } else if (question.question_type === "multi_select") {
      setAnswer([])
    } else {
      setAnswer("N/A")
    }
  }, [question])

  return (
    <div className="card card-normal bordered px-4 glass">
      <div className="card-body flex flex-col items-center">
        <h2 className="card-title">{question.text}</h2>

        <div className="form-control">
          {question.question_type === "single_select" && (
            <select
              className="select w-full max-w-xs select-bordered"
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
            >
              <option disabled selected>
                Choose an option
              </option>
              {question.options.map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
          )}
          {question.question_type === "numeric_input" && (
            <input
              type="number"
              className="input input-bordered w-full max-w-xs"
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
            />
          )}
          {question.question_type === "multi_select" && (
            // TODO: Add multi-select question function
            <div className="max-h-80 sm:max-h-60 md:max-h-36 overflow-auto">
              <div className="flex flex-col">
                {question.options.map((option) => (
                  <label
                    className="label cursor-pointer flex items-center"
                    key={option}
                  >
                    <span className="label-text">{option}</span>
                    <input
                      type="checkbox"
                      className="checkbox mx-2"
                      onChange={() => handleCheckboxChange(option)}
                    />
                  </label>
                ))}
              </div>
            </div>
          )}
          {question.question_type === "text_input" && (
            <input
              type="text"
              className="input input-bordered w-full max-w-xs"
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
            />
          )}
        </div>

        <button
          className="btn btn-primary w-fit mx-auto mt-4"
          onClick={() => {
            // console.log({ answer })
            onClickNext(answer)
          }}
        >
          {isLast ? "Submit" : "Next"}
        </button>
      </div>
    </div>
  )
}

const NewPlanPage: NextPage = () => {
  const [currentQuestionId, setCurrentQuestionId] = useState<number>(1)
  const [answers, setAnswers] = useState<Record<number, string | string[]>>({})

  console.log({
    answers,
  })

  return (
    <main className="flex flex-col items-center min-h-screen justify-center p-2">
      <div>
        <Question
          question={questions[currentQuestionId - 1]}
          isLast={currentQuestionId === questions.length}
          onClickNext={(answer: string | string[]) => {
            if (currentQuestionId === questions.length) {
              alert("Submitted!")
              return
            }

            setAnswers({ ...answers, [currentQuestionId]: answer })
            setCurrentQuestionId(currentQuestionId + 1)
          }}
        />
      </div>

      <ul className="steps mx-auto mt-8 gap-4">
        {formSections.map((section) => (
          <li
            key={section}
            className={`step ${
              currentQuestionId >= sectionBreakpoints[section] && "step-primary"
            }`}
          >
            {section}
          </li>
        ))}
      </ul>
    </main>
  )
}

export default NewPlanPage
