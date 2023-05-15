'use client';

import { NextPage } from 'next';
import { FC, useEffect, useState } from 'react';

import questionsFile from '../../questions.json';

const { questions } = questionsFile as {
  questions: Question[];
};

interface Question {
  id: number;
  section: FormSection;
  text: string;
  options: string[];
  question_type: 'single_select' | 'open_text';
}

type FormSection = 'Personal Characteristics' | 'History' | 'Goals';
const formSections: FormSection[] = [
  'Personal Characteristics',
  'History',
  'Goals',
];
const sectionBreakpoints = {
  'Personal Characteristics': 1,
  History: 7,
  Goals: 14,
};

const Question: FC<{
  question: Question;
  isLast: boolean;
  onClickNext: (answer: string) => void;
}> = ({ question, isLast, onClickNext }) => {
  const [answer, setAnswer] = useState<string>(question.options?.[0] || '');

  useEffect(() => {
    setAnswer(question.options?.[0] || '');
  }, [question]);

  return (
    <div className='card bordered'>
      <div className='card-body'>
        <h2 className='card-title'>{question.text}</h2>
        {/* <p className='card-text'>
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Quisquam
          necessitatibus incidunt ut officiis explicabo inventore.
        </p> */}

        <div className='form-control'>
          {question.question_type === 'single_select' && (
            <select
              className='select w-full max-w-xs select-bordered'
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
            >
              <option disabled selected>
                Pick an answer
              </option>
              {question.options.map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
          )}
          {question.question_type === 'open_text' && (
            <input
              type='text'
              className='input input-bordered w-full max-w-xs'
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
            />
          )}
        </div>

        <button
          className='btn btn-primary w-fit mx-auto mt-4'
          onClick={() => {
            console.log({ answer });
            onClickNext(answer);
          }}
        >
          {isLast ? 'Submit' : 'Next'}
        </button>
      </div>
    </div>
  );
};

const NewPlanPage: NextPage = () => {
  const [currentQuestionId, setCurrentQuestionId] = useState<number>(1);
  const [answers, setAnswers] = useState<Record<number, string>>({});

  console.log({
    answers,
  });

  return (
    <main className='flex flex-col'>
      <div className='mt-16'>
        <Question
          question={questions[currentQuestionId - 1]}
          isLast={currentQuestionId === questions.length}
          onClickNext={(answer: string) => {
            if (currentQuestionId === questions.length) {
              alert('Submitted!');
              return;
            }

            setAnswers({ ...answers, [currentQuestionId]: answer });
            setCurrentQuestionId(currentQuestionId + 1);
          }}
        />
      </div>

      <ul className='steps mx-auto mt-8'>
        {formSections.map((section) => (
          <li
            key={section}
            className={`step ${
              currentQuestionId >= sectionBreakpoints[section] && 'step-primary'
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
