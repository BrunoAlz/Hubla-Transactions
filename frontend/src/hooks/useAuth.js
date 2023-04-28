import { useState, useEffect } from "react";
import { useSelector } from "react-redux";

export const useAuth = () => {
  const { user } = useSelector((state) => state.auth);
  console.log(user)

  const [auth, setAuth] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (user) {
      console.log("AUTHHHHH TRUEEE");
      setAuth(true);
    } else {
      console.log("AUTHHHHH FALSE");
      setAuth(false);
    }

    setLoading(false);
  }, [user]);

  return { auth, loading };
};
