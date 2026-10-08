"""Launch with: python -m streamlit run scripts/review_calibration.py"""
from pathlib import Path
import json
import sys

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from skillfreq.calibration_review import (
    EVIDENCE_FIELDS, ISSUE_TAGS, SIGNALS, SUBGRADE_OPTIONS, SUMMARY_FIELDS, build_queue, changes,
    compact_requirement_evidence,
    default_review_path, find_review, identity, load_comparison, load_reviews, save_review, text,
)


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OLD = ROOT / 'data/outputs/results-db-90-days-requirements.csv'
DEFAULT_NEW = ROOT / 'data/outputs/results-db-90-days-requirement-semantics.csv'


def comparison_table(row, fields):
    def display(value):
        try:
            value = json.loads(value)
        except (ValueError, TypeError):
            return value or '—'
        if isinstance(value, dict):
            # Repeated source spans and group audits belong in the details expander.
            value = compact_requirement_evidence(value)
            return '\n'.join(f'{k.replace("_", " ")}: {text(v)}' for k, v in value.items()) or 'None'
        if isinstance(value, list):
            return '; '.join(text(v.get('matched_terms', v)) if isinstance(v, dict) else text(v)
                             for v in value) or 'None'
        return text(value)

    values = [{'Field': f.replace('_', ' ').capitalize(),
               'OLD': display(row.get('old_' + f)), 'NEW': display(row.get('new_' + f))}
              for f in fields if row.get('old_' + f) or row.get('new_' + f)]
    if values:
        st.table(values)


def main():
    st.set_page_config(page_title='SkillFreq calibration review', layout='centered')
    st.title('Calibration review')
    # Clear only the departed editor; values are restored from saved reviews.
    for widget in st.session_state.pop('clear_editor', []):
        st.session_state.pop(widget, None)
    with st.sidebar.form('queue_options'):
        mode = st.selectbox('Input format', ['Two grading exports', 'One comparison file'])
        before = st.text_input('OLD export path', str(DEFAULT_OLD))
        after = st.text_input('NEW export / comparison path', str(DEFAULT_NEW))
        output = st.text_input('Review output path (blank = find existing or create dated file)', '')
        signals = st.multiselect('Include any of these changes', SIGNALS, default=list(SIGNALS[:4]))
        threshold = st.number_input('Minimum absolute fit-score change', min_value=0.0, value=5.0)
        limit = st.number_input('Total review target', min_value=1, max_value=10000, value=100,
                                help='Saved reviews for this comparison count toward this total.')
        sample = st.number_input('Unchanged sanity sample', min_value=0, max_value=100, value=5,
                                 help='Included within the total target. Previously reviewed unchanged jobs count toward this sample.')
        status = st.selectbox('Review status', ['Unreviewed', 'All', 'Reviewed'])
        load = st.form_submit_button('Load / rebuild queue')
    if load:
        try:
            with st.spinner('Reading saved grading output…'):
                rows, message = load_comparison(Path(after), Path(before) if mode == 'Two grading exports' else None)
                path = Path(output).resolve() if output.strip() else default_review_path(rows[0])
                if path.suffix.lower() != '.xlsx':
                    raise ValueError('Review output must end in .xlsx.')
                if path in [Path(p).resolve() for p in (before, after) if p.strip()]:
                    raise ValueError('Review output must be separate from the input files.')
                reviews = load_reviews(path, rows[0])
                queue = build_queue(rows, reviews, signals, threshold, limit, sample, status)
                st.session_state.run = dict(queue=queue, reviews=reviews, path=path, message=message,
                                            index=0, threshold=threshold, target=limit, status=status,
                                            comparison_keys={identity(r) for r in rows},
                                            records={identity(r): r for r in rows}, editing_key=None)
                for key in list(st.session_state):
                    if key.startswith('edit_'):
                        del st.session_state[key]
        except (OSError, ValueError, KeyError) as error:
            st.error(str(error))
            st.stop()
    if 'run' not in st.session_state:
        st.info('Choose saved grading exports or an OLD/NEW comparison file, then load a targeted queue.')
        st.stop()
    run = st.session_state.run
    if 'records' not in run:
        st.info('Click Load / rebuild queue to load the updated review controls.')
        st.stop()
    with st.sidebar.form('existing_review'):
        st.markdown('**Edit existing review**')
        lookup_id = st.text_input('Job ID')
        load_existing = st.form_submit_button('Load review')
    if load_existing:
        try:
            fresh_reviews = load_reviews(run['path'], next(iter(run['records'].values())))
            existing = find_review(fresh_reviews, lookup_id)
            existing_key = identity(existing)
            if existing_key not in run['records']:
                raise LookupError('The saved review was found, but its job evidence is missing from the loaded comparison.')
            run['reviews'] = fresh_reviews
            run['editing_key'] = existing_key
            # Reload saved values even when reopening the same job with unsaved edits.
            for widget in list(st.session_state):
                if widget.startswith('edit_'):
                    del st.session_state[widget]
        except LookupError as error:
            st.sidebar.warning(str(error))
        except (OSError, ValueError) as error:
            st.sidebar.error(str(error))
    editing = run['editing_key'] is not None
    if editing and st.sidebar.button('Return to review queue'):
        run['editing_key'] = None
        for widget in list(st.session_state):
            if widget.startswith('edit_'):
                del st.session_state[widget]
        st.rerun()
    queue, reviews = run['queue'], run['reviews']
    st.caption(run['message'])
    st.caption(f"Reviews: {run['path']}")
    if 'notice' in st.session_state:
        st.info(st.session_state.pop('notice'))
    completed = len(run['comparison_keys'] & reviews.keys())
    target = run['target']
    st.progress(min(completed / target, 1.0), text=f'{completed} / {target} total records reviewed')
    if completed >= target:
        st.success('Review target reached. Increase the total review target to review more jobs, or choose All / Reviewed to revisit saved work.')
    if not queue and not editing:
        if completed < target:
            st.info('No records match. Adjust the filters or choose All / Reviewed to revisit saved work.')
        st.stop()
    pending = sum(identity(r) not in reviews for r in queue)
    st.caption(f'{pending} unreviewed records in this queue.')
    if not editing and run['status'] != 'Reviewed' and completed + pending < target:
        st.info('The current filters provide fewer records than needed to reach the target. Adjust the filters to include more jobs.')
    row = run['records'][run['editing_key']] if editing else queue[run['index']]
    key = identity(row)
    saved = reviews.get(key, {})
    if editing:
        st.info(f'Editing existing review: {key[1]}')
    else:
        st.caption(f"Record {run['index'] + 1} of {len(queue)} · {'Reviewed' if saved else 'Unreviewed'}")
    st.subheader(row['title'] or 'Untitled job')
    st.text(f"Company: {row['company'] or 'Not available'}\nSource: {key[0] or 'Not available'}\nJob ID: {key[1]}")
    if row.get('source'):
        st.text(row['source'])
    signals = [s for s, changed in changes(row, run['threshold']).items() if changed]
    st.caption(', '.join(signals) or 'Unchanged sanity sample / small score change')
    comparison_table(row, SUMMARY_FIELDS)
    with st.expander('Description / requirements', expanded=True):
        with st.container(height=300):
            st.text(row.get('description') or 'Description not available in this export.')
        if row.get('old_description'):
            st.warning('The description also changed between exports.')
            st.text('OLD description\n' + row['old_description'])
    with st.expander('Grading evidence and reasons', expanded=True):
        comparison_table(row, EVIDENCE_FIELDS)
    with st.expander('Detailed requirement groups'):
        for side in ('old', 'new'):
            for field in ('missing_required_skills', 'missing_preferred_skills'):
                try:
                    evidence = json.loads(row.get(side + '_' + field, ''))
                except (ValueError, TypeError):
                    continue
                if isinstance(evidence, dict) and evidence.get('requirement_groups'):
                    st.caption(f'{side.upper()} — {field.replace("_", " ")}')
                    st.json(evidence['requirement_groups'], expanded=False)
    with st.expander('Grading versions'):
        comparison_table(row, ('grading_version',))
    st.caption('Save records explicitly. Previous / Next discard unsaved edits. Rebuild the queue to refresh filters.')
    st.caption('Calibration mindset: judge whether the NEW result is justified by the posting and your configured rules.')
    with st.expander('Calibration mindset — reminder'):
        st.markdown(
            "Judge whether SkillFreq's **NEW result** is justified by the job posting and your configured rules.\n\n"
            "Do **not** grade based on:\n\n"
            "- whether you personally like the job\n"
            "- whether you would apply today\n"
            "- whether you think a recruiter would hire you\n\n"
            '**Ask:** Given what this posting says and the rules SkillFreq is supposed to follow, '
            'is the NEW result correct?'
        )
    editor = 'edit_' + repr(key)
    with st.form('review_' + repr(key)):
        rating = st.radio('Overall rating', [1, 2, 3], index=int(saved['review_rating']) - 1 if saved else None,
                          format_func=lambda n: {1: '1 = Good — better or correct', 2: '2 = Neutral / Unclear',
                                                 3: '3 = Bad — worse or incorrect'}[n], key=editor + '_rating',
                          help='Is the NEW grading behavior an improvement over OLD according to the posting '
                               'and configured rules? Neutral / Unclear includes mixed results, both OLD and '
                               'NEW being defensible, or insufficient evidence.')
        subgrades = {}
        for field, label, help_text in (
            ('decision_quality', 'Decision quality',
             "Is the NEW apply/manual-review/skip decision justified by the posting and SkillFreq's rules? "
             'Compare NEW with OLD, not whether you personally would apply.'),
            ('score_quality', 'Score quality',
             'Does the NEW fit score reasonably reflect the evidence in the posting? Consider matched and '
             'missing requirements, seniority, hard filters, and skills/stack evidence.'),
            ('requirement_interpretation', 'Requirement interpretation',
             'Did SkillFreq correctly interpret the requirement structure in the posting? Check required vs '
             'preferred, alternatives (AWS, Azure, or GCP), grouped requirements, equivalent technologies, '
             'and ambiguous wording. Were preferences treated as mandatory or alternatives counted separately?'),
        ):
            options = SUBGRADE_OPTIONS[field]
            value = saved.get(field)
            subgrades[field] = st.selectbox(label, options, index=options.index(value) if value in options else None,
                                           key=editor + '_' + field, help=help_text,
                                           placeholder='Choose a judgment', format_func=lambda v: v.replace('_', ' '))
        saved_tags = [t for t in text(saved.get('issue_tags')).split(';') if t]
        tags = st.multiselect('Issue tags (optional)', list(dict.fromkeys(ISSUE_TAGS + saved_tags)),
                              default=saved_tags, key=editor + '_tags')
        note = st.text_area('Review note (optional)', text(saved.get('review_note')), key=editor + '_note')
        st.caption('For 2 or 3, please add a note or issue tag explaining the uncertainty or problem. Saving is still allowed without one.')
        buttons = st.columns(4)
        previous = buttons[0].form_submit_button('Previous', disabled=editing or run['index'] == 0)
        save = buttons[1].form_submit_button('Save')
        save_next = buttons[2].form_submit_button('Save + Next', disabled=editing)
        next_item = buttons[3].form_submit_button('Next', disabled=editing or run['index'] == len(queue)-1)
    if save or save_next:
        try:
            run['reviews'] = save_review(run['path'], row, rating, note, tags,
                                         require_existing=editing, **subgrades)
        except (OSError, ValueError) as error:
            st.error(f'Not saved: {error}. If the workbook is open in Excel, close it and retry.')
            st.stop()
        st.session_state.notice = 'Existing review updated.' if editing else 'Review saved.'
        if rating in (2, 3) and not note.strip() and not tags:
            st.session_state.notice += ' Consider adding a note or issue tag for this rating.'
        if save_next and run['index'] == len(queue)-1:
            st.session_state.notice += ' End of queue. Increase the target or adjust filters and rebuild to review more jobs.'
    if previous or next_item or save_next:
        run['index'] = max(0, min(len(queue)-1, run['index'] + (-1 if previous else 1)))
    if previous or next_item or save or save_next:
        st.session_state.clear_editor = [editor + suffix for suffix in
                                         ('_rating', '_tags', '_note', *(f'_{f}' for f in SUBGRADE_OPTIONS))]
        st.rerun()


if __name__ == '__main__':
    main()
