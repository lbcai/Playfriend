import { useState, useEffect } from 'react';
import './ContactForm.css';

function ContactForm() {

    const [comments, setComments] = useState('');
    const [email, setEmail] = useState('');
    const [type, setType] = useState('');
    const [validationErrors, setValidationErrors] = useState([]);
    const [hasSubmitted, setHasSubmitted] = useState(false);

    useEffect(() => {
        const errors = [];
        const regex = new RegExp(/^[a-zA-Z0-9]+@(?:[a-zA-Z0-9]+\.)+[A-Za-z]+$/);
        if (!regex.test(email)) errors.push('Please provide a valid email.')
        if (!type.length) errors.push('Please select a submission category.')
        if (!comments.length) errors.push('Please include more information about your submission.')
        setValidationErrors(errors);
    }, [email, type, comments])

    const onSubmit = (e) => {
        e.preventDefault();

        setHasSubmitted(true);

        if (validationErrors.length) return;

        const information = {
            email,
            type,
            comments,
            submittedOn: new Date()
        };

        fetch('/send', {
            method: 'POST',
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify(information)
        })
        .then((response) => response.json())
        .then((json) => {
            if (json.result) {
                setEmail('');
                setType('');
                setComments('');
                setValidationErrors([]);
                setHasSubmitted(false);
                return alert(`Thank you for your feedback!`);
            } else {
                return alert(`There was an error. Please try again later.`);
            }
        })
        .catch((e) => {return alert(`There was an error. Please try again later.`)});

    }

    return (
        <div>
            {hasSubmitted && validationErrors.length > 0 && (
                <div className='list-div'>
                    The following errors were found:
                    <ul>
                        {validationErrors.map(error => (
                        <li key={error}>{error}</li>
                        ))}
                    </ul>
                </div>
            )}

            <form onSubmit={onSubmit}>

                <div>
                    <label htmlFor='email'>Email: </label>
                    <br></br>
                    <input
                        className='input-email'
                        id='email'
                        type='text'
                        onChange={e => setEmail(e.target.value)}
                        value={email}
                        placeholder="Email Address"
                        />
                </div>

                <div>
                    <label htmlFor='type'>Category: </label>
                    <br></br>
                    <select
                        className='select-type'
                        name='type'
                        onChange={e => setType(e.target.value)}
                        value={type}
                    >
                        <option value='' disabled>
                        Select...
                        </option>
                        <option>Bug Report</option>
                        <option>Suggestion</option>
                        <option>Feedback</option>
                    </select>
                </div>

                <div>
                    <textarea
                        className='textarea-comment'
                        id='comments'
                        name='comments'
                        onChange={e => setComments(e.target.value)}
                        value={comments}
                        placeholder="Comments"
                    />
                </div>

                <button>Submit</button>

            </form>
        </div>
    );

}

export default ContactForm;
