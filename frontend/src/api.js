const server = 'http://127.0.0.1:8000/';
const apiUrl = `${server}api/v1/`;
const authRes = `${apiUrl}auth/`;
const eventsRes = `${apiUrl}events/`;


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

  return await response.json();
}

export async function signUp(email, password)
{
  let response = await fetch(`${authRes}sign_in/`, {
    method: 'POST',
    body: JSON.stringify({username: email, password: password})
  });

  return await response.json();
}

export async function listEvents()
{
  let response = await fetch(eventsRes);

  return await response.json();
}
