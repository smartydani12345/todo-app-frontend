// "use client";

// import { useState } from "react";
// import apiClient from '@/lib/api-client';

// export default function Register() {
//   const [name, setName] = useState("");
//   const [email, setEmail] = useState("");
//   const [password, setPassword] = useState("");
//   const [confirmPassword, setConfirmPassword] = useState("");
//   const [errorMessage, setErrorMessage] = useState("");
//   const [loading, setLoading] = useState(false);

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     setErrorMessage("");
//     setLoading(true);

//     // Debugging – state check karo
//     console.log("Form state at submit:", { name, email, password, confirmPassword });

//     const trimmedEmail = email.trim();
//     const trimmedPassword = password.trim();
//     const trimmedConfirm = confirmPassword.trim();

//     if (!trimmedEmail) {
//       setErrorMessage("Email is required");
//       setLoading(false);
//       return;
//     }

//     if (!trimmedPassword) {
//       setErrorMessage("Password is required");
//       setLoading(false);
//       return;
//     }

//     if (trimmedPassword !== trimmedConfirm) {
//       setErrorMessage("Passwords do not match");
//       setLoading(false);
//       return;
//     }

//     console.log("Sending to backend:", { email: trimmedEmail, password: trimmedPassword });

//     try {
//       // Prepare form data to match backend expectations
//       const formData = new URLSearchParams({
//         email: trimmedEmail,
//         password: trimmedPassword,
//         name: name
//       });

//       const response = await apiClient.post('/auth/register', formData.toString(), {
//         headers: {
//           'Content-Type': 'application/x-www-form-urlencoded',
//         }
//       });

//       console.log("Backend success:", response.data);

//       // Save the access token to localStorage
//       localStorage.setItem('access_token', response.data.access_token);

//       alert("Registration successful! Redirecting to dashboard...");
//       window.location.href = "/tasks";
//     } catch (error) {
//       console.error("Full error:", error);

//       let errorText = "Something went wrong. Please try again.";

//       if (error.response?.data?.detail) {
//         const detail = error.response.data.detail;
//         errorText = Array.isArray(detail)
//           ? detail.map(d => d.msg || d.type || "Validation error").join(", ")
//           : detail;
//       } else if (error.message) {
//         errorText = error.message;
//       }

//       setErrorMessage(errorText);
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
//       <div className="max-w-md w-full space-y-8 bg-white p-10 rounded-xl shadow-2xl">
//         <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
//           Create your account
//         </h2>

//         {errorMessage && (
//           <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-4">
//             <p className="text-red-700">{errorMessage}</p>
//           </div>
//         )}

//         <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
//           <div className="rounded-md shadow-sm -space-y-px">
//             <div>
//               <label htmlFor="name" className="sr-only">Full Name</label>
//               <input
//                 id="name"
//                 name="name"
//                 type="text"
//                 autoComplete="name"
//                 value={name}
//                 onChange={(e) => setName(e.target.value)}
//                 className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
//                 placeholder="Full Name"
//               />
//             </div>
//             <div>
//               <label htmlFor="email" className="sr-only">Email address</label>
//               <input
//                 id="email"
//                 name="email"
//                 type="email"
//                 autoComplete="email"
//                 required
//                 value={email}
//                 onChange={(e) => setEmail(e.target.value)}
//                 className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
//                 placeholder="Email address"
//               />
//             </div>
//             <div>
//               <label htmlFor="password" className="sr-only">Password</label>
//               <input
//                 id="password"
//                 name="password"
//                 type="password"
//                 autoComplete="new-password"
//                 required
//                 value={password}
//                 onChange={(e) => setPassword(e.target.value)}
//                 className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
//                 placeholder="Password"
//               />
//             </div>
//             <div>
//               <label htmlFor="confirm-password" className="sr-only">Confirm Password</label>
//               <input
//                 id="confirm-password"
//                 name="confirm-password"
//                 type="password"
//                 autoComplete="new-password"
//                 required
//                 value={confirmPassword}
//                 onChange={(e) => setConfirmPassword(e.target.value)}
//                 className="appearance-none rounded-b-md relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
//                 placeholder="Confirm Password"
//               />
//             </div>
//           </div>

//           <div>
//             <button
//               type="submit"
//               disabled={loading}
//               className={`group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white ${
//                 loading ? "bg-blue-400 cursor-not-allowed" : "bg-blue-600 hover:bg-blue-700"
//               } focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors`}
//             >
//               {loading ? "Signing up..." : "Sign up"}
//             </button>
//           </div>
//         </form>

//         <div className="text-center text-sm text-gray-600 mt-4">
//           Already have an account?{" "}
//           <a href="/login" className="font-medium text-blue-600 hover:text-blue-500">
//             Sign in
//           </a>
//         </div>
//       </div>
//     </div>
//   );
// }
'use client';

import { useState } from "react";
import { useRouter } from "next/navigation";
import apiClient from "../../lib/api-client";
import { setToken } from "../../lib/tokenUtils";
import toast from 'react-hot-toast';
import Link from 'next/link';

export default function RegisterPage() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const router = useRouter();

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    // Validate passwords match
    if (password !== confirmPassword) {
      setError("Passwords do not match");
      toast.error("Passwords do not match");
      return;
    }

    try {
      // Prepare form data to match backend expectations (form-data)
      const formData = new FormData();
      formData.append('name', name.trim());
      formData.append('email', email.trim());
      formData.append('password', password.trim());

      const response = await apiClient.post("/auth/register", formData);

      // Save token using utility function and redirect to Phase 2 dashboard
      // Backend returns both user info and access_token in response
      if (response.data.access_token) {
        setToken(response.data.access_token);
        toast.success('Registration successful! Redirecting to dashboard...');
        router.push("/tasks"); // Redirect to Phase 2 dashboard
      } else if (response.data.token) {
        // Alternative token field name
        setToken(response.data.token);
        toast.success('Registration successful! Redirecting to dashboard...');
        router.push("/tasks"); // Redirect to Phase 2 dashboard
      } else {
        // If token wasn't returned in response, try to get from localStorage
        toast.success('Registration successful! Redirecting to dashboard...');
        router.push("/tasks"); // Redirect to Phase 2 dashboard
      }
    } catch (err: any) {
      console.error(err);
      let errorMessage = "Registration failed";
      if (err.response?.data?.detail) {
        errorMessage = err.response.data.detail;
      } else if (err.message) {
        errorMessage = err.message;
      }
      setError(errorMessage);
      toast.error(errorMessage);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-500 mb-2">
            TODO EVOLUTION
          </h1>
          <h2 className="text-xl font-bold text-white">
            Create Account
          </h2>
        </div>
        {error && <div className="text-red-500 text-center">{error}</div>}
        <form className="mt-8 space-y-6" onSubmit={handleRegister}>
          <div className="space-y-4">
            <div>
              <input
                type="text"
                placeholder="Full Name"
                value={name}
                required
                onChange={(e) => setName(e.target.value)}
                className="w-full rounded-lg bg-gray-800 border border-gray-700 py-3 px-4 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div>
              <input
                type="email"
                placeholder="Email"
                value={email}
                required
                onChange={(e) => setEmail(e.target.value)}
                className="w-full rounded-lg bg-gray-800 border border-gray-700 py-3 px-4 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div>
              <input
                type="password"
                placeholder="Password"
                value={password}
                required
                onChange={(e) => setPassword(e.target.value)}
                className="w-full rounded-lg bg-gray-800 border border-gray-700 py-3 px-4 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div>
              <input
                type="password"
                placeholder="Confirm Password"
                value={confirmPassword}
                required
                onChange={(e) => setConfirmPassword(e.target.value)}
                className="w-full rounded-lg bg-gray-800 border border-gray-700 py-3 px-4 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>
          <button
            type="submit"
            className="w-full bg-gradient-to-r from-purple-500 to-pink-600 text-white py-3 rounded-lg hover:from-purple-600 hover:to-pink-700 transition-all duration-300"
          >
            Register
          </button>
        </form>
        <div className="text-center text-sm text-gray-400 mt-4">
          Already have an account?{' '}
          <Link href="/login" className="font-medium text-blue-400 hover:text-blue-300 transition-colors">
            Sign in
          </Link>
        </div>
        <div className="text-center text-sm text-gray-500 mt-6">
          <Link href="/" className="font-medium text-gray-400 hover:text-gray-300 transition-colors">
            ← Back to Home
          </Link>
        </div>
      </div>
    </div>
  );
}
