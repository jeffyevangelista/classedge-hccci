export const sendRefreshToken = (res: Response, payload: any) => {
  const refreshToken = generateRefreshToken(payload);

  res.cookie("refreshToken", refreshToken, {
    httpOnly: true,
    sameSite: "strict",
    secure: NODE_ENV !== "development",
    maxAge: 1000 * 60 * 60 * 24 * 7,
  });
};
