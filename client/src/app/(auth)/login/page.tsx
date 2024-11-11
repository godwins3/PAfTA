'use client';
import axios from 'axios';
// Formik
import { useFormik } from 'formik';
import * as yup from 'yup';
// Material UI
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Link from 'next/link'; // Ensure this is the Link from Next.js
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import Header from '../../../components/Nav/Nav';
import { en } from '../../../../translations';
import { useRouter } from 'next/navigation';

const theme = createTheme();

const validationSchema = yup.object({
    email: yup
        .string()
        .required('Email is required')
        .email('Enter a valid email'),
    password: yup
        .string()
        .min(8, 'Password should be of minimum 8 characters length')
        .required('Password is required'),
});

export default function Login() {
    const router = useRouter()
    const a = en;

    const inLocalStorage = (user: { token: string }) => {
        window.localStorage.setItem('token', JSON.stringify(user.token));
    };

    const formik = useFormik({
        onSubmit: async (data) => {
            await axios.post('http://localhost:3000/client/authenticate', {
                email: data.email,
                password: data.password
            }).then((response) => {
                inLocalStorage(response.data);
                router.push('/'); // Now you can use router.push correctly
            }).catch(error => {
                console.error('Error authenticating:', error);
            });
        },
        validationSchema,
        validateOnMount: true,

        initialValues: {
            email: '',
            password: ''
        }
    });

    return (
        <ThemeProvider theme={theme}>
            <Header home={true} />
            <Container classes={{ root: 'cont' }} component="main" maxWidth="xs">
                <Box
                    sx={{
                        marginTop: 15,
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                    }}
                >
                    <Typography component="h1" variant="h5">
                        {a.title}
                    </Typography>

                    <form onSubmit={formik.handleSubmit}>
                        <TextField
                            autoFocus
                            required
                            fullWidth
                            margin="normal"
                            id="email"
                            label={a.inputEmail}
                            name="email"
                            autoComplete="email"
                            value={formik.values.email}
                            onChange={formik.handleChange}
                            onBlur={formik.handleBlur}
                            disabled={formik.isSubmitting}
                        />
                        {(formik.touched.email && formik.errors.email) && (
                            <span style={{ color: 'red', fontSize: '14px' }}>{formik.errors.email}</span>
                        )}

                        <TextField
                            required
                            fullWidth
                            margin="normal"
                            name="password"
                            label={a.inputPassword}
                            type="password"
                            id="password"
                            autoComplete="current-password"
                            value={formik.values.password}
                            onChange={formik.handleChange}
                            onBlur={formik.handleBlur}
                            disabled={formik.isSubmitting}
                        />
                        {(formik.touched.password && formik.errors.password) && (
                            <span style={{ color: 'red', fontSize: '14px' }}>{formik.errors.password}</span>
                        )}
                        <Button
                            type="submit"
                            fullWidth
                            variant="contained"
                            sx={{ mt: 3, mb: 2 }}
                            disabled={formik.isSubmitting || !formik.isValid}
                        >
                            {a.signinButton}
                        </Button>

                        <Grid container>
                            <Grid item>
                                <Link href="/signup">{a.signinLink}</Link> {/* Link works without <a> */}
                            </Grid>
                        </Grid>
                    </form>
                </Box>
            </Container>
        </ThemeProvider>
    );
}
