"use client";

import { NextPage } from "next";
import { FC, useContext, useEffect, useState } from "react";
import Select from "react-select";

import questionsFile from "../../questions.json";
import { getServer, getWorkoutPlan } from "../utils";
import { APIResponse, Answer } from "../types";
import { SupabaseClient, createClient } from "@supabase/supabase-js";
import { Database } from "../supabase";

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
  "Goals & Preferences": 7,
  "Physical Constraints": 17,
};

const formatMultiOptions = (options: string[]) => {
  return options.map((option) => ({ label: option, value: option }));
};

const Question: FC<{
  question: Question;
  isLast: boolean;
  isLoading: boolean;
  onClickNext: (answer: Answer) => Promise<void>;
  onClickBack?: () => void;
  selectedAnswer: Answer;
}> = ({
  question,
  isLast,
  isLoading,
  onClickNext,
  onClickBack,
  selectedAnswer,
}) => {
  const [answer, setAnswer] = useState<Answer>(
    selectedAnswer ||
      (question.question_type === "multi_select"
        ? [question.options?.[0]]
        : question.options?.[0] || "")
  );

  useEffect(() => {
    if (question.question_type === "single_select") {
      setAnswer(selectedAnswer || question.options?.[0]);
    } else if (question.question_type === "multi_select") {
      setAnswer(selectedAnswer || [question.options?.[0]]);
    } else if (question.question_type === "numeric_input") {
      setAnswer(selectedAnswer || "50");
    } else {
      setAnswer(selectedAnswer || "N/A");
    }
  }, [question, selectedAnswer]);

  return (
    <div className="card card-normal bordered px-8 glass">
      <div className="card-body flex flex-col items-center">
        <div className="flex items-center w-full">
          <div className="absolute left-4 m-2 pb-2">
            {question.id !== 1 && (
              <button
                className={"btn btn-circle btn-outline btn-xs"}
                onClick={onClickBack}
                disabled={isLoading}
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-4 w-4"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M15 19l-7-7 7-7"
                  />
                </svg>
              </button>
            )}
          </div>
          <h2 className="card-title">{question.text}</h2>
        </div>

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
            <div className="flex">
              <Select
                isMulti
                closeMenuOnSelect={false}
                options={formatMultiOptions(question.options)}
                defaultValue={formatMultiOptions(question.options)[0]}
                className="select-bordered z-100 w-full max-w-xs"
                onChange={(values) => {
                  setAnswer(values.map((value) => value.value));
                }}
              />
            </div>
          )}
        </div>

        <button
          className={`btn btn-primary w-fit mx-auto mt-4 ${
            isLoading ? "loading" : ""
          }`}
          onClick={() => {
            // console.log({ answer })
            onClickNext(answer);
          }}
        >
          {isLoading ? "Generating..." : isLast ? "Submit" : "Next"}
        </button>
      </div>
    </div>
  );
};

const Loader: FC<{}> = ({}) => {
  return (
    <div className="mt-4 alert bg-secondary text-secondary-content shadow-md">
      <div>
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          className="stroke-current flex-shrink-0 w-6 h-6"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth="2"
            d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
          ></path>
        </svg>
        <span>
          💭 Please wait while we generate your personalized workout plan...
        </span>
      </div>
    </div>
  );
};

const insertPlanDatabase = async (
  supabase: SupabaseClient,
  response: APIResponse
) => {
  const { data, error } = await supabase
    .from("plans")
    .insert({ response: response })
    .select();

  return data;
};

const NewPlanPage: NextPage = () => {
  const [currentQuestionId, setCurrentQuestionId] = useState<number>(1);
  const [answers, setAnswers] = useState<Record<number, Answer>>({});
  const [loading, setLoading] = useState<boolean>(false);

  const supabase = createClient<Database>(
    "https://wibpwiyydrvuhrcpqjhi.supabase.co",
    process.env.NEXT_PUBLIC_SUPABASE_KEY as string
  );

  useEffect(() => {
    (async () => {
      const server = await getServer();
      // console.log("SERVER: ", server);
      if (server.status === 200) {
        console.log("Server online!");
      }
    })();

    return () => {};
  }, []);

  return (
    <main className="flex flex-col items-center min-h-screen justify-center z-10 p-2">
      <div>
        <Question
          question={questions[currentQuestionId - 1]}
          isLast={currentQuestionId === questions.length}
          isLoading={loading}
          onClickNext={async (answer: Answer) => {
            const newAnswers = { ...answers, [currentQuestionId]: answer };
            setAnswers(newAnswers);
            if (currentQuestionId === questions.length) {
              setLoading(true);
              const data: APIResponse = await getWorkoutPlan({
                answer: newAnswers,
              });

              const newRow = await insertPlanDatabase(supabase, data);
              // pass this data to the result page
              window.location.href = `/result?plan_id=${encodeURIComponent(
                newRow![0].id
              )}`;
              // console.log(newRow[0].id);
              setLoading(false);
              return;
            }
            setCurrentQuestionId((prevId) => prevId + 1);
          }}
          onClickBack={() => {
            setCurrentQuestionId((prevId) => prevId - 1);
          }}
          selectedAnswer={answers[currentQuestionId]}
        />
      </div>

      {loading ? (
        <Loader />
      ) : (
        <ul className="steps steps-vertical md:steps-horizontal mx-auto -z-10 mt-8 gap-4">
          {formSections.map((section) => (
            <li
              key={section}
              className={`step  ${
                currentQuestionId >= sectionBreakpoints[section] &&
                "step-primary"
              }`}
            >
              {section}
            </li>
          ))}
        </ul>
      )}

      {/* Show answers */}
      {/* <div className="overflow-x-auto max-h-32 my-4">
        <table className="table table-compact">
          <thead>
            <th>Question</th>
            <th>Answer</th>
          </thead>
          <tbody>
            {Object.entries(answers).map(([key, value]) => (
              <tr key={key}>
                <td>{key}</td>
                <td>{value}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div> */}
    </main>
  );
};

export default NewPlanPage;
