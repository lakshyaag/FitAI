import { NextPage } from 'next';
import { FC } from 'react';

const calculateTabIndex = (weekNumber: number, dayNumber: number) => {
  // TODO: 4 is the number of weeks in one cycle. This should be dynamic.
  return weekNumber * 4 + dayNumber + 1;
};

const generatedWorkout: APIResponse = {
  wks: [
    {
      wk_range: 'Week 1-4',
      days: [
        {
          num: 1,
          focus: 'Upper Body',
          exs: [
            {
              name: 'Push-ups',
              type: 'Bodyweight',
              sets: '3',
              reps: '10',
              dur: null,
            },
            {
              name: 'Dumbbell Bicep Curls',
              type: 'Dumbbells',
              sets: '3',
              reps: '12',
              dur: null,
            },
            {
              name: 'Plank',
              type: 'Bodyweight',
              sets: null,
              reps: null,
              dur: {
                val: 30,
                unit: 'seconds',
              },
            },
          ],
        },
        {
          num: 2,
          focus: 'Lower Body',
          exs: [
            {
              name: 'Bodyweight Squats',
              type: 'Bodyweight',
              sets: '4',
              reps: '8',
              dur: null,
            },
            {
              name: 'Lunges',
              type: 'Bodyweight',
              sets: '3',
              reps: '10',
              dur: null,
            },
            {
              name: 'Jumping Jacks',
              type: 'Cardio',
              sets: null,
              reps: null,
              dur: {
                val: 1,
                unit: 'minute',
              },
            },
          ],
        },
        {
          num: 3,
          focus: 'Rest Day',
          exs: null,
        },
        {
          num: 4,
          focus: 'Full Body',
          exs: [
            {
              name: 'Burpees',
              type: 'Bodyweight',
              sets: '3',
              reps: '10',
              dur: null,
            },
            {
              name: 'Deadlift',
              type: 'Barbells',
              sets: '3',
              reps: '8',
              dur: null,
            },
            {
              name: 'Mountain Climbers',
              type: 'Bodyweight',
              sets: null,
              reps: null,
              dur: {
                val: 30,
                unit: 'seconds',
              },
            },
          ],
        },
      ],
    },
    {
      wk_range: 'Week 5-8',
      days: [
        {
          num: 1,
          focus: 'Upper Body',
          exs: [
            {
              name: 'Push-ups',
              type: 'Bodyweight',
              sets: '4',
              reps: '12',
              dur: null,
            },
            {
              name: 'Dumbbell Bicep Curls',
              type: 'Dumbbells',
              sets: '4',
              reps: '12',
              dur: null,
            },
            {
              name: 'Plank',
              type: 'Bodyweight',
              sets: null,
              reps: null,
              dur: {
                val: 45,
                unit: 'seconds',
              },
            },
          ],
        },
        {
          num: 2,
          focus: 'Lower Body',
          exs: [
            {
              name: 'Bodyweight Squats',
              type: 'Bodyweight',
              sets: '4',
              reps: '10',
              dur: null,
            },
            {
              name: 'Lunges',
              type: 'Bodyweight',
              sets: '4',
              reps: '12',
              dur: null,
            },
            {
              name: 'Jumping Jacks',
              type: 'Cardio',
              sets: null,
              reps: null,
              dur: {
                val: 1,
                unit: 'minute',
              },
            },
          ],
        },
        {
          num: 3,
          focus: 'Rest Day',
          exs: null,
        },
        {
          num: 4,
          focus: 'Full Body',
          exs: [
            {
              name: 'Burpees',
              type: 'Bodyweight',
              sets: '4',
              reps: '12',
              dur: null,
            },
            {
              name: 'Deadlift',
              type: 'Barbells',
              sets: '4',
              reps: '8',
              dur: null,
            },
            {
              name: 'Mountain Climbers',
              type: 'Bodyweight',
              sets: null,
              reps: null,
              dur: {
                val: 45,
                unit: 'seconds',
              },
            },
          ],
        },
      ],
    },
  ],
  notes: [
    {
      content: 'Warm-up for 5-10 minutes before each workout session.',
    },
    {
      content: 'Stretch for 5 minutes after each workout session.',
    },
    {
      content: 'Adjust the number of sets and reps according to your progress.',
    },
    {
      content:
        'Consult a healthcare professional before starting any fitness program.',
    },
  ],
};

interface IWeek {
  wk_range: string;
  days: IDay[];
}

interface IDay {
  num: number;
  focus: string;
  exs:
    | {
        name: string;
        type: string;
        sets: string | null;
        reps: string | null;
        dur: {
          val: number;
          unit: string;
        } | null;
      }[]
    | null;
}

export interface APIResponse {
  wks: IWeek[];
  notes: {
    content: string;
  }[];
}

const WeekDisplay: FC<{ week: IWeek; weekNumber: number }> = ({
  week,
  weekNumber,
}) => {
  return (
    <div>
      <h3 className='text-2xl font-bold'>{week.wk_range}</h3>
      <div className='flex flex-col gap-4 mt-4'>
        {week.days.map((day) => (
          <DayDisplay key={day.num} day={day} weekNumber={weekNumber} />
        ))}
      </div>
    </div>
  );
};

const formatSetsRepsDuration = (
  sets: string | null,
  reps: string | null,
  dur: {
    val: number;
    unit: string;
  } | null
) => {
  // eg. 3x10
  if (sets && reps) {
    return `${sets}x${reps}`;
  }

  // eg. 3x30s
  if (sets && dur) {
    return `${sets}x${dur.val}${dur.unit}`;
  }
};

const DayDisplay: FC<{ day: IDay; weekNumber: number }> = ({
  day,
  weekNumber,
}) => {
  return (
    <div
      tabIndex={calculateTabIndex(weekNumber, day.num - 1)}
      className='collapse collapse-arrow border border-base-300 bg-base-100 rounded-box'
    >
      <div className='collapse-title text-xl font-medium'>
        Day {day.num} - {day.focus}
      </div>
      <div className='collapse-content'>
        {day.exs ? (
          <ul className='list-disc list-inside'>
            {day.exs.map((ex) => (
              <li key={ex.name}>
                {ex.name} ({ex.type}){' '}
                <span>{formatSetsRepsDuration(ex.sets, ex.reps, ex.dur)}</span>
              </li>
            ))}
          </ul>
        ) : (
          <p>Rest day</p>
        )}
      </div>
    </div>
  );
};

const ResultPage: NextPage = ({}) => {
  // const generatedWorkout = decodeURIComponent(query.workout);

  return (
    <main>
      <h1 className='text-4xl font-bold'>Generated workout</h1>

      <div className='divider' />

      <div className='flex flex-col gap-8'>
        {generatedWorkout.wks.map((week) => (
          <WeekDisplay
            key={week.wk_range}
            week={week}
            weekNumber={generatedWorkout.wks.indexOf(week)}
          />
        ))}
      </div>

      <div className='divider' />

      <h3 className='text-2xl font-bold'>Notes</h3>
      <ul className='list-disc list-inside'>
        {generatedWorkout.notes.map((note) => (
          <li key={note.content}>{note.content}</li>
        ))}
      </ul>
    </main>
  );
};

export default ResultPage;
