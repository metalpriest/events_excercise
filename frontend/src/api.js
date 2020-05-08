import {csrftoken} from './csrf'

const server = 'http://127.0.0.1:8000/';
const apiUrl = `${server}api/v1/`;
const authRes = `${apiUrl}auth/`;
const eventsRes = `${apiUrl}events/`;


let headers = new Headers();
headers.append('X-CSRFToken', csrftoken);
headers.append('Content-Type', 'application/json');


export async function checkSession()
{
  let response = await fetch(`${authRes}check_session/`, {
    method: 'GET',
  });
  return await response.json();
}

export async function login(email, password)
{
  let response = await fetch(`${authRes}sign_in/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    credentials: 'include',
    body: JSON.stringify({username: email, password: password})
  });

  return await response;
}

export async function signUp(email, password)
{
  let response = await fetch(`${authRes}sign_up/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    credentials: 'include',
    body: JSON.stringify({username: email, password: password})
  });

  return await response;
}

export async function logout() {
  let response = await fetch(`${authRes}logout/`, {
    method: 'GET',
    credentials: 'include'
  });

  return response;
}

export async function listEvents()
{
  let response = await fetch(eventsRes);

  return await response.json();
}


export async function participate(eventId)
{
  let response = await fetch(`${eventsRes}${eventId}/participate/`, {
    method: 'POST',
    headers: headers,
    credentials: 'include'
  });

  return response.status === 204;
}

export async function withdraw(eventId)
{
  let response = await fetch(`${eventsRes}${eventId}/withdraw/`, {
    method: 'POST',
    headers: headers,
    credentials: 'include'
  });

  return response.status === 204;
}

export async function createEvent(data)
{
  let {title, description, date_start} = data;
  let response = await fetch(`${eventsRes}`, {
    method: 'POST',
    headers: headers,
    credentials: 'include',
    body: JSON.stringify({title, description, date_start})
  });

  return response;
}

export async function updateEvent(data)
{

  let response = await fetch(`${eventsRes}/${data.id}/`, {
    method: 'POST',
    headers: headers,
    credentials: 'include',
    body: JSON.stringify(data)
  });

  return response;
}
