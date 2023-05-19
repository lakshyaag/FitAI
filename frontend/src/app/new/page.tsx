"use client";

import { NextPage } from "next";
import { FC, useContext, useEffect, useState } from "react";
import Select from "react-select";

import questionsFile from "../../questions.json";
import { getWorkoutPlan } from "../utils";

type Answer = string | string[];

const { questions } = questionsFile as {
  questions: Question[];
};

interface Question {
  id: number;
  section: FormSection;
  text: string;
  options: string[];
  question_type:
    | "single_select"
    | "text_input"
    | "multi_select"
    | "numeric_input";
}

type FormSection =
  | "Personal Information"
  | "Fitness History"
  | "Goals & Preferences"
  | "Physical Constraints";
const formSections: FormSection[] = [
  "Personal Information",
  "Fitness History",
  "Goals & Preferences",
  "Physical Constraints",
];
const sectionBreakpoints = {
  "Personal Information": 1,
  "Fitness History": 5,
  "Goals & Preferences": 8,
  "Physical Constraints": 17,
};

const formatMultiOptions = (options: string[]) => {
  return options.map((option) => ({ label: option, value: option }));
};

const Question: FC<{
  question: Question;
  isLast: boolean;
  onClickNext: (answer: Answer) => Promise<void>;
}> = ({ question, isLast, onClickNext }) => {
  const [answer, setAnswer] = useState<Answer>(
    question.question_type ? [] : question.options?.[0] || ""
  );

  useEffect(() => {
    if (question.question_type === "single_select") {
      setAnswer(question.options?.[0]);
    } else if (question.question_type === "multi_select") {
      setAnswer([]);
    } else if (question.question_type === "numeric_input") {
      setAnswer("50");
    } else {
      setAnswer("N/A");
    }
  }, [question]);

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
          {question.question_type === "text_input" && (
            <input
              type="text"
              className="input input-bordered w-full max-w-xs"
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
            />
          )}
          {question.question_type === "numeric_input" && (
            <input
              type="text"
              className="input input-bordered w-full max-w-xs"
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
            />
          )}
          {question.question_type === "multi_select" && (
            <Select
              isMulti
              options={formatMultiOptions(question.options)}
              className="select select-bordered z-20"
              onChange={(values) => {
                setAnswer(values.map((value) => value.value));
              }}
            />
          )}
        </div>

        <button
          className="btn btn-primary w-fit mx-auto mt-4"
          onClick={() => {
            // console.log({ answer })
            onClickNext(answer);
          }}
        >
          {isLast ? "Submit" : "Next"}
        </button>
      </div>
    </div>
  );
};

const NewPlanPage: NextPage = () => {
  const [currentQuestionId, setCurrentQuestionId] = useState<number>(1);
  const [answers, setAnswers] = useState<Record<number, Answer>>({});

  return (
    <main className="flex flex-col items-center min-h-screen justify-center p-2">
      <div>
        <Question
          question={questions[currentQuestionId - 1]}
          isLast={currentQuestionId === questions.length}
          onClickNext={async (answer: Answer) => {
            setAnswers({ ...answers, [currentQuestionId]: answer });
            if (currentQuestionId === questions.length) {
              const data = await getWorkoutPlan({ answer: answers });
              // pass this data to the result page
              window.location.href = `/result?workout=${encodeURIComponent(
                JSON.stringify(data)
              )}`;
              return;
            }
            setCurrentQuestionId(currentQuestionId + 1);
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
  );
};

export default NewPlanPage;
