import { useState } from 'react';
import './ContactForm.css';

function ContactForm() {

    const [comments, setComments] = useState('');
    const [email, setEmail] = useState('');
    const [type, setType] = useState('');

    const onSubmit = e => {
        e.preventDefault();

        const information = {
            email,
            type,
            comments,
            submittedOn: new Date()
        };

        setEmail('');
        setType('');
        setComments('');
    }

    return (
        <form onSubmit={onSubmit}>

            <div>
                <label htmlFor='email'>Email: </label>
                <br></br>
                <input className='input-email' id='email' type='text' onChange={e => setEmail(e.target.value)} value={email} placeholder="Email Address"/>
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
                    Select a category...
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
    );

}

export default ContactForm;
