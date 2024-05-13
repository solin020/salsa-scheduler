/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { MultipleChoiceCheckbox } from './MultipleChoiceCheckbox';
import type { SingleChoiceDropdown } from './SingleChoiceDropdown';
import type { SingleChoiceRadio } from './SingleChoiceRadio';
import type { Slider } from './Slider';
import type { Textbox } from './Textbox';
export type QuestionType = (Textbox | Slider | SingleChoiceDropdown | SingleChoiceRadio | MultipleChoiceCheckbox)
export type Ema = {
    type: 'ema';
    id: string;
    form: QuestionType[];
};

